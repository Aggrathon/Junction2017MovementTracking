package com.example.infa.suuntoapp;

import android.Manifest;
import android.app.Activity;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class FileLog {

	public static final String DIRECTORY_NAME = "MoveSense";
	public static String LOG_DIRECTORY = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS) + File.separator + DIRECTORY_NAME;

	public static void createFolders(Activity activity) {
		File logDir = new File(LOG_DIRECTORY);
		logDir.mkdirs();
		if(logDir.isDirectory()) {
		}
		else {	
			Log.e("Storage", "Could not access storage to create directories");
			Toast.makeText(activity, "Could not access storage to create directories", Toast.LENGTH_LONG).show();
		}
	}
	public static void createLogfile(final Activity activity, final String logs, final String filename) {
		createFolders(activity);
		BufferedWriter writer;
		try {
			writer = new BufferedWriter(new FileWriter(LOG_DIRECTORY + File.separator + filename));
			writer.write(logs);
			writer.close();
		}
		catch (IOException e) {
			Log.e("Storage", "Could not write logfiles ("+e.getLocalizedMessage()+")");
			Toast.makeText(activity, "Could not access storage to write log", Toast.LENGTH_LONG).show();
		}
	}

}
