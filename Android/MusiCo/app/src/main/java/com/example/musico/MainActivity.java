package com.example.musico;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //temp for testing
        Intent test = new Intent(getApplicationContext(), RecommendActivity.class);
        startActivity(test);

        Button rgst_button = findViewById(R.id.btn_register);
        rgst_button.setOnClickListener(v -> {
            Intent activity2Intent = new Intent(getApplicationContext(), RegisterActivity.class);
            startActivity(activity2Intent);
        });
    }
}