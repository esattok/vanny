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
    }

    public void openActivity2() {
        Intent intent = new Intent(this, SettingsPage.class);
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
}
