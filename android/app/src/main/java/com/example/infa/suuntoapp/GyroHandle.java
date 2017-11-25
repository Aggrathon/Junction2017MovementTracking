package com.example.infa.suuntoapp;

import android.app.Activity;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.movesense.mds.MdsException;
import com.movesense.mds.MdsNotificationListener;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by henriksoderberg on 25/11/2017.
 */

public class GyroHandle implements MdsNotificationListener {

    private String url;
    private RequestQueue queue;

    public GyroHandle(Activity gyr){
        queue = Volley.newRequestQueue(gyr);
        url = "http://172.20.10.13:5000";
    }

    @Override
    public void onNotification(String s) {
        StringRequest stringRequest = new StringRequest(Request.Method.POST,
                url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("===SEND ERROR===", error.toString());
            }
        }){
            @Override
            protected Map<String, String> getParams(){
                Map<String, String> params = new HashMap<>();
                params.put("test", s);

                return params;
            }
        };
        queue.add(stringRequest);
        Log.d("=== GYRO DATA LOG : ", s);
    }

    @Override
    public void onError(MdsException e) {
        Log.d("=== DATA LOG ERROR : ", e.toString());
    }
}
