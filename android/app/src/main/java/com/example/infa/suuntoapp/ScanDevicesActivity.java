package com.example.infa.suuntoapp;

import android.bluetooth.BluetoothClass;
import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.support.v4.app.ActivityCompat;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.support.v4.content.ContextCompat;
import android.widget.ListView;

import com.movesense.mds.Mds;
import com.movesense.mds.MdsConnectionListener;
import com.movesense.mds.MdsException;
import com.movesense.mds.MdsResponseListener;
import com.polidea.rxandroidble.RxBleClient;
import com.polidea.rxandroidble.RxBleDevice;
import com.polidea.rxandroidble.scan.ScanSettings;

import java.util.ArrayList;

import rx.Subscription;

public class ScanDevicesActivity extends AppCompatActivity implements AdapterView.OnItemClickListener, AdapterView.OnItemLongClickListener{
    private static final int MY_PERMISSIONS_REQUEST_LOCATION = 1;
    private static final String LOG_TAG = MainActivity.class.getSimpleName();

    static private RxBleClient bleClient;

    public static DeviceScanResult device;
    public static Mds mds;
    public static final String SCHEME_PREFIX = "suunto://";

    private ListView scanResultListView;
    private ArrayList<DeviceScanResult> scanResultList = new ArrayList<>();
    ArrayAdapter<DeviceScanResult> scanResultAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_devices);

        scanResultListView = (ListView)findViewById(R.id.devicesList);
        scanResultAdapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, scanResultList);
        scanResultListView.setAdapter(scanResultAdapter);
        scanResultListView.setOnItemClickListener(this);

        // Make sure we have all the permissions this app needs
        requestNeededPermissions();

        // Initialize Movesense MDS library
        initMds();
    }


    private void initMds() {
        mds = Mds.builder().build(this);
    }

    void requestNeededPermissions()
    {
        // Here, thisActivity is the current activity
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {

            // No explanation needed, we can request the permission.
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                    MY_PERMISSIONS_REQUEST_LOCATION);

        }
    }

    private RxBleClient getBleClient() {
        // Init RxAndroidBle (Ble helper library) if not yet initialized
        if (bleClient == null)
        {
            bleClient = RxBleClient.create(this);
        }

        return bleClient;
    }

    Subscription ScanSubscription;
    public void onScanClicked(View view) {
        findViewById(R.id.scanButton).setVisibility(View.GONE);
        findViewById(R.id.stopScanButton).setVisibility(View.VISIBLE);

        // Start with empty list
        scanResultList.clear();
        scanResultAdapter.notifyDataSetChanged();

        ScanSubscription = getBleClient().scanBleDevices(
                new ScanSettings.Builder()
                        // .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY) // change if needed
                        // .setCallbackType(ScanSettings.CALLBACK_TYPE_ALL_MATCHES) // change if needed
                        .build()
                // add filters if needed
        )
                .subscribe(
                        scanResult -> {
                            Log.d(LOG_TAG,"scanResult: " + scanResult);

                            // Process scan result here. filter movesense devices.
                            if (scanResult.getBleDevice()!=null &&
                                    scanResult.getBleDevice().getName() != null &&
                                    scanResult.getBleDevice().getName().startsWith("Movesense")) {

                                // replace if exists already, add otherwise
                                DeviceScanResult msr = new DeviceScanResult(scanResult);
                                if (scanResultList.contains(msr))
                                    scanResultList.set(scanResultList.indexOf(msr), msr);
                                else
                                    scanResultList.add(0, msr);

                                scanResultAdapter.notifyDataSetChanged();
                            }
                        },
                        throwable -> {
                            Log.e(LOG_TAG,"scan error: " + throwable);
                            // Handle an error here.

                            // Re-enable scan buttons, just like with ScanStop
                            onScanStopClicked(null);
                        }
                );
    }
    public void onScanStopClicked(View view) {
        if (ScanSubscription != null)
        {
            ScanSubscription.unsubscribe();
            ScanSubscription = null;
        }

        findViewById(R.id.scanButton).setVisibility(View.VISIBLE);
        findViewById(R.id.stopScanButton).setVisibility(View.GONE);
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        if (position < 0 || position >= scanResultList.size())
            return;

        device = scanResultList.get(position);
        if (!device.isConnected()) {
            // Stop scanning
            onScanStopClicked(null);
            // And connect to the device
            connectBLEDevice(device);
        }
        else {
            // Device is connected, trigger showing /Info
            //showDeviceInfo(device.connectedSerial);
            Intent i = new Intent(getApplicationContext(), DataShowActivity.class);
            startActivity(i);
        }
    }

    @Override
    public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
        if (position < 0 || position >= scanResultList.size())
            return false;

        DeviceScanResult device = scanResultList.get(position);

        Log.i(LOG_TAG, "Disconnecting from BLE device: " + device.macAddress);
        mds.disconnect(device.macAddress);

        return true;
    }

    private void connectBLEDevice(DeviceScanResult device) {
        RxBleDevice bleDevice = getBleClient().getBleDevice(device.macAddress);

        Log.i(LOG_TAG, "Connecting to BLE device: " + bleDevice.getMacAddress());
        mds.connect(bleDevice.getMacAddress(), new MdsConnectionListener() {

            @Override
            public void onConnect(String s) {
                Log.d(LOG_TAG, "onConnect:" + s);
            }

            @Override
            public void onConnectionComplete(String macAddress, String serial) {
                for (DeviceScanResult sr : scanResultList) {
                    if (sr.macAddress.equalsIgnoreCase(macAddress)) {
                        sr.markConnected(serial);
                        break;
                    }
                }
                scanResultAdapter.notifyDataSetChanged();
            }

            @Override
            public void onError(MdsException e) {
                Log.e(LOG_TAG, "onError:" + e);

                showConnectionError(e);
            }

            @Override
            public void onDisconnect(String bleAddress) {
                Log.d(LOG_TAG, "onDisconnect: " + bleAddress);
                for (DeviceScanResult sr : scanResultList) {
                    if (bleAddress.equals(sr.macAddress))
                        sr.markDisconnected();
                }
                scanResultAdapter.notifyDataSetChanged();
            }
        });
    }

    void showDeviceInfo(final String serial) {
        String uri = SCHEME_PREFIX + serial + "/Info";
        final Context ctx = this;
        mds.get(uri, null, new MdsResponseListener() {
            @Override
            public void onSuccess(String s) {
                Log.i(LOG_TAG, "Device " + serial + " /info request succesful: " + s);
                // Display info in alert dialog
                AlertDialog.Builder builder = new AlertDialog.Builder(ctx);
                builder.setTitle("Device info:")
                        .setMessage(s)
                        .show();
            }

            @Override
            public void onError(MdsException e) {
                Log.e(LOG_TAG, "Device " + serial + " /info returned error: " + e);
            }
        });
    }

    private void showConnectionError(MdsException e) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this)
                .setTitle("Connection Error:")
                .setMessage(e.getMessage());

        builder.create().show();
    }
}
