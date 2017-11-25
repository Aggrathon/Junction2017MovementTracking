package com.example.infa.suuntoapp;

import com.polidea.rxandroidble.RxBleDevice;
import com.polidea.rxandroidble.scan.ScanResult;

import java.io.Serializable;

/**
 * Created by henriksoderberg on 25/11/2017.
 */

public class DeviceScanResult implements Serializable {
    public int rssi;
    public String macAddress;
    public String name;
    public String connectedSerial;

    public DeviceScanResult(ScanResult scanResult) {
        this.macAddress = scanResult.getBleDevice().getMacAddress();
        this.rssi = scanResult.getRssi();
        this.name = scanResult.getBleDevice().getName();
    }

    public boolean isConnected() {return connectedSerial != null;}
    public void markConnected(String serial) {connectedSerial = serial;}
    public void markDisconnected() {connectedSerial = null;}

    public boolean equals(Object object) {
        if(object instanceof DeviceScanResult && ((DeviceScanResult)object).macAddress.equals(this.macAddress)) {
            return true;
        }
        else if(object instanceof RxBleDevice && ((RxBleDevice)object).getMacAddress().equals(this.macAddress)) {
            return true;
        } else {
            return false;
        }
    }

    public String toString() {
        return (isConnected()?"*** ":"") + macAddress + " - " + name + " [" + rssi + "]" + (isConnected()?" ***":"");
    }
}
