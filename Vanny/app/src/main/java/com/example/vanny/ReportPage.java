package com.example.vanny;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

public class ReportPage extends AppCompatActivity {
    private ImageButton backBtn;
    private Button reportFileBtn;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_report_page);

        backBtn = (ImageButton) findViewById(R.id.backBtn);
        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity2();
            }
        });

        reportFileBtn = (Button) findViewById(R.id.reportOne);
        reportFileBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity3();
            }
        });
    }

    public void openActivity2(){
        Intent intent = new Intent(this, SettingsPage.class);
        startActivity(intent);
    }

    public void openActivity3(){
        Intent intent = new Intent(this, ReportFile.class);
        startActivity(intent);
    }
}