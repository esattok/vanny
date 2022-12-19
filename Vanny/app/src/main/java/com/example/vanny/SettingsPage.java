package com.example.vanny;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

public class SettingsPage extends AppCompatActivity {

    private ImageButton backBtn;
    private Button safetyBtn;
    private Button notificationBtn;
    private Button lullabyBtn;
    private Button alarmBtn;
    private Button videoBtn;
    private Button reportBtn;
    private Button audioBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings_page);

        backBtn = (ImageButton) findViewById(R.id.backBtn);
        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity2();
            }
        });

        safetyBtn = (Button) findViewById(R.id.safetyBtn);
        safetyBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity3();
            }
        });

        notificationBtn = (Button) findViewById(R.id.notificationsBtn);
        notificationBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity4();
            }
        });

        lullabyBtn = (Button) findViewById(R.id.lullabyBtn);
        lullabyBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity5();
            }
        });

        alarmBtn = (Button) findViewById(R.id.alarmsBtn);
        alarmBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity6();
            }
        });

        videoBtn = (Button) findViewById(R.id.videosBtn);
        videoBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity7();
            }
        });

        reportBtn = (Button) findViewById(R.id.reportBtn);
        reportBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity8();
            }
        });

        audioBtn = (Button) findViewById(R.id.audioBtn);
        audioBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity9();
            }
        });
    }


    public void openActivity2() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }

    public void openActivity3() {
        Intent intent = new Intent(this, safetyPage.class);
        startActivity(intent);
    }

    public void openActivity4() {
        Intent intent = new Intent(this, NotificationPage.class);
        startActivity(intent);
    }

    public void openActivity5() {
        Intent intent = new Intent(this, LullabyPage.class);
        startActivity(intent);
    }

    public void openActivity6() {
        Intent intent = new Intent(this, AlarmPage.class);
        startActivity(intent);
    }
    public void openActivity7() {
        Intent intent = new Intent(this, VideoPage.class);
        startActivity(intent);
    }
    public void openActivity8() {
        Intent intent = new Intent(this, ReportPage.class);
        startActivity(intent);
    }

    public void openActivity9() {
        Intent intent = new Intent(this, AudioPage.class);
        startActivity(intent);
    }
}
