package com.example.infa.suuntoapp;

import android.util.Log;

import com.movesense.mds.MdsException;
import com.movesense.mds.MdsNotificationListener;

/**
 * Created by henriksoderberg on 25/11/2017.
 */

public class LinearAccHandle implements MdsNotificationListener {

    @Override
    public void onNotification(String s) {
        Log.d("=== LINEAR DATA LOG : ", s);
    }

    @Override
    public void onError(MdsException e) {
        Log.d("=== DATA LOG ERROR ===", e.getMessage().toString());
    }
}
