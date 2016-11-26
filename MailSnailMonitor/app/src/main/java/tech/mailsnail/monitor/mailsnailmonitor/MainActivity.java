package tech.mailsnail.monitor.mailsnailmonitor;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.Picture;
import android.graphics.SurfaceTexture;
import android.hardware.Camera;
import android.media.Image;
import android.os.Environment;
import android.provider.ContactsContract;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import net.bozho.easycamera.DefaultEasyCamera;
import net.bozho.easycamera.EasyCamera;

import java.io.File;
import java.io.FileOutputStream;
import java.util.Collections;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends AppCompatActivity {

    ImageView imageView;
    SurfaceTexture surface;
    EasyCamera camera;
    EasyCamera.CameraActions actions;
    EasyCamera.PictureCallback callback;
    Bitmap lastPhoto;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        surface = new SurfaceTexture(0);
        imageView = (ImageView) findViewById(R.id.imageView);

        camera = DefaultEasyCamera.open();
        Camera.Parameters p = camera.getParameters();
        p.setFocusMode(Camera.Parameters.FOCUS_MODE_MACRO);
        List<Camera.Size> sizes = p.getSupportedPictureSizes();
        p.setPictureSize(1280, 720);
        p.setFlashMode(Camera.Parameters.FLASH_MODE_ON);
        camera.setParameters(p);
        try {
            actions = camera.startPreview(surface);
        } catch (Exception e) {
            e.printStackTrace();
        }

        callback = new EasyCamera.PictureCallback() {
            @Override
            public void onPictureTaken(byte[] bytes, EasyCamera.CameraActions cameraActions) {
                File file = new File(MainActivity.this.getExternalFilesDir(Environment.DIRECTORY_PICTURES), "test.jpg");
                Log.d("MMM", file.getAbsolutePath());
                try {
                    FileOutputStream out = new FileOutputStream(file);
                    out.write(bytes);
                    out.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }

                Bitmap photo = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                imageView.setImageBitmap(photo);
                if (lastPhoto != null) {
                    if (areDifferent(lastPhoto, photo)) {
                        Toast.makeText(MainActivity.this, "Changed!", Toast.LENGTH_SHORT).show();
                    }
                }
                lastPhoto = photo;
            }
        };

        actions.getCamera().autoFocus(new Camera.AutoFocusCallback() {
            @Override
            public void onAutoFocus(boolean success, Camera camera) {
                Timer timer = new Timer();
                timer.schedule(new TimerTask() {

                    int times = 0;

                    @Override
                    public void run() {
                        if (times < 10) {
                            actions.takePicture(EasyCamera.Callbacks.create().withJpegCallback(callback));
                            times += 1;
                        } else {
                            this.cancel();
                        }
                    }
                }, 3000, 10000);
            }
        });

        findViewById(R.id.button).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                actions.takePicture(EasyCamera.Callbacks.create().withJpegCallback(callback));
            }
        });

    }

    //Returns whether two images are the same or not
    private boolean areDifferent(Bitmap image1, Bitmap image2) {
        if (image1.getWidth() != image2.getWidth() || image1.getHeight() != image2.getHeight()) {
            return false;
        } else {
            int[] pixels1 = new int[image1.getWidth() * image1.getHeight()];
            int[] pixels2 = new int[image2.getWidth() * image2.getHeight()];
            long diffRed = 0;
            long diffGreen = 0;
            long diffBlue = 0;
            image1.getPixels(pixels1, 0, image1.getWidth(), 0, 0, image1.getWidth(), image1.getHeight());
            image2.getPixels(pixels2, 0, image2.getWidth(), 0, 0, image2.getWidth(), image2.getHeight());

            for (int i = 0; i < image1.getWidth() * image1.getHeight(); i++) {
                int pixel1 = pixels1[i];
                int pixel2 = pixels2[i];
                diffRed += Math.abs(Color.red(pixel1) - Color.red(pixel2));
                diffGreen += Math.abs(Color.green(pixel1) - Color.green(pixel2));
                diffBlue += Math.abs(Color.blue(pixel1) - Color.blue(pixel2));
            }

            diffRed /= pixels1.length;
            diffGreen /= pixels1.length;
            diffBlue /= pixels1.length;
            float avgDiff = (diffRed + diffGreen + diffBlue) / 3f;

            Log.d("MSM", String.valueOf(avgDiff));

            //Toast.makeText(this, String.valueOf(avgDiff), Toast.LENGTH_SHORT).show();

            if (avgDiff >= 10) {
                return true;
            } else {
                return false;
            }
        }
    }



    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);


    }

    @Override
    protected void onPause() {
        super.onPause();
        camera.close();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        camera.close();
    }


}
