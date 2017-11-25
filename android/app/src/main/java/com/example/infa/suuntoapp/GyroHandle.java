package com.example.infa.suuntoapp;

import android.util.Log;

import com.movesense.mds.MdsException;
import com.movesense.mds.MdsNotificationListener;

import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by henriksoderberg on 25/11/2017.
 */

public class GyroHandle implements MdsNotificationListener {

    /*
    URL url;
    HttpURLConnection urlConnection = null;

    public GyroHandle(){
        try {
            //url = new URL("http://172.20.10.13:5000");
            //urlConnection = (HttpURLConnection) url.openConnection();
            JsonObjectRequest jsonObjectRequest
        } catch(Exception e){
            //SOMETHING
        }
    }
    */

    @Override
    public void onNotification(String s) {
        Log.d("=== GYRO DATA LOG : ", s);
    }

    @Override
    public void onError(MdsException e) {
        Log.d("=== DATA LOG ERROR : ", e.toString());
    }
}
