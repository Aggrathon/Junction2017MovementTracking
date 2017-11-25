package com.example.infa.suuntoapp;

import android.bluetooth.BluetoothClass;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import com.movesense.mds.Mds;
import com.movesense.mds.MdsNotificationListener;
import com.movesense.mds.MdsSubscription;

import rx.Subscription;

public class DataShowActivity extends AppCompatActivity {

    private Mds mds;
    private MdsSubscription accSubscription;
    private MdsSubscription gyroSubscription;
    private DeviceScanResult device;

    public static final String URI_CONNECTEDDEVICES = "suunto://MDS/ConnectedDevices";
    public static final String URI_EVENTLISTENER = "suunto://MDS/EventListener";

    private final String LINEAR_ACC_PATH = "Meas/Acc/26";
    private final String ANGULAR_VELOCITY_PATH = "Meas/Gyro/26";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_data_show);

        device = ScanDevicesActivity.device;
        mds = ScanDevicesActivity.mds;

        StringBuilder sb = new StringBuilder();
        String accUri = sb.append("{\"Uri\": \"").append(device.connectedSerial).append("/").append(LINEAR_ACC_PATH).append("\"}").toString();

        StringBuilder sb2 = new StringBuilder();
        String gyroUri = sb2.append("{\"Uri\": \"").append(device.connectedSerial).append("/").append(ANGULAR_VELOCITY_PATH).append("\"}").toString();

        gyroSubscription = mds.subscribe(
                URI_EVENTLISTENER,
                gyroUri,
                new GyroHandle(this)
        );


        accSubscription = mds.subscribe(
                URI_EVENTLISTENER,
                accUri,
                new LinearAccHandle(this)
                );
    }
}
