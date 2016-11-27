package com.muki;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import com.muki.core.MukiCupApi;
import com.muki.core.MukiCupCallback;
import com.muki.core.model.Action;
import com.muki.core.model.DeviceInfo;
import com.muki.core.model.ErrorCode;
import com.muki.core.model.ImageProperties;
import com.muki.core.util.ImageUtils;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {

    private String mCupId;
    private MukiCupApi mMukiCupApi;
    private int temp = 15;
    private static final String SERIAL = "0004180";
    private static final String URL_UNREAD_MAIL = "http://85.188.13.246:8080/test";
    private Timer checkForMailTimer;
    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {


            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, temp);

        }

        imageView = (ImageView) findViewById(R.id.imageView_preview);
        imageView.setImageResource(R.drawable.cooldown);

        mMukiCupApi = new MukiCupApi(getApplicationContext(), new MukiCupCallback() {
            @Override
            public void onCupConnected() {
                showToast("Cup connected");
            }

            @Override
            public void onCupDisconnected() {
                showToast("Cup disconnected");
            }

            @Override
            public void onDeviceInfo(DeviceInfo deviceInfo) {  }

            @Override
            public void onImageCleared() {
                showToast("Image cleared");
            }

            @Override
            public void onImageSent() {
                showToast("Image sent");
            }

            @Override
            public void onError(Action action, ErrorCode errorCode) {
                showToast("Error:" + errorCode + " on action:" + action);
            }
        });

        sendImage(BitmapFactory.decodeResource(this.getResources(), R.drawable.cooldown),
                new DoAfter() {

                    @Override
                    void toDo() {
                        TimerTask tt = new TimerTask() {
                            @Override
                            public void run() {
                                checkForMail();
                            }
                        };
                        checkForMailTimer = new Timer();
                        checkForMailTimer.schedule(tt, 1000, 5000);
                    }

                });

        findViewById(R.id.button_reset).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mCupId != null) {
                    imageView.setImageResource(R.drawable.cooldown);
                    mMukiCupApi.clearImage(mCupId);
                }
            }
        });

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == temp) {
            if (grantResults.length > 0
                    && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                //We could do something here if we wanted to
            }
        }
    }

    private void checkForMail() {
        new AsyncTask<Void, Void, Integer>() {
            @Override
            protected Integer doInBackground(Void... params) {
                HttpURLConnection urlConnection;
                try {
                    URL url = new URL(URL_UNREAD_MAIL);
                    urlConnection = (HttpURLConnection) url.openConnection();
                    int response = urlConnection.getResponseCode();

                    if (response != HttpURLConnection.HTTP_OK) {
                        Log.e("MSM", "Failed to download mail");
                        return -1;
                    }

                    BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder total = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        total.append(line).append('\n');
                    }

                    String result = total.toString();
                    try {
                        int count = Integer.valueOf(result);
                        return count;
                    } catch (NumberFormatException e) {
                        Log.e("MMM", "Unable to parse unread count: " + result + ". " + e.getMessage());
                        return 0;
                    }

                } catch (Exception e) {
                    Log.e("MMM", "Failed to check for new mail: " + e.getMessage());
                }

                return 0;
            }

            @Override
            protected void onPostExecute(Integer count) {
                if (count > 0) {
                    showToast("You have received mail!");
                    sendImage(BitmapFactory.decodeResource(MainActivity.this.getResources(), R.drawable.mail0), new DoAfter());
                }
            }
        }.execute();
    }

    public void sendImage(final Bitmap bitmap, final DoAfter toDo) {
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                try {
                    return MukiCupApi.cupIdentifierFromSerialNumber(SERIAL);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return null;
            }

            @Override
            protected void onPostExecute(String s) {
                if (s != null) {
                    mCupId = s;
                    Log.d("MSC", "Loaded the image");
                    Bitmap scaled = ImageUtils.scaleBitmapToCupSize(bitmap);
                    Log.d("MSC", "Scaled the image");
                    ImageUtils.convertImageToCupImage(scaled, ImageProperties.DEFAULT_CONTRACT);
                    Log.d("MSC", "Converted the image");
                    try {
                        mMukiCupApi.sendImage(scaled, s);
                        Log.d("MSC", "Sent the image");
                    } catch (Exception e) {
                        Log.e("MSC", "Unable to send the image: " + e.getMessage());
                    }
                } else {
                    Log.e("MMM", "Unable to get cup id");
                }
                toDo.toDo();
            }
        }.execute();
    }

    private void showToast(String text) {
        Toast.makeText(this, text, Toast.LENGTH_SHORT).show();
    }


}

class DoAfter {

    void toDo() {};

}