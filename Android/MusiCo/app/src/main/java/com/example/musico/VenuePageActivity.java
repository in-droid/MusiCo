package com.example.musico;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class VenuePageActivity extends AppCompatActivity {

    private RecyclerView eventsRecycler;
    private JSONArray testArr;
    private int id;
    private String name;
    private String venueInfo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_venue_page);

        eventsRecycler = findViewById(R.id.venueEventsList);

        try {
            testArr = createTestArray();
        } catch (JSONException e) {
            e.printStackTrace();
        }

        setAdapter();

        id = Integer.parseInt((String) getIntent().getSerializableExtra("venueID"));
        name = (String) getIntent().getSerializableExtra("venueName");
        venueInfo = (String) getIntent().getSerializableExtra("venueInfo");

        TextView info = findViewById(R.id.venuePageInfo);
        TextView venueName = findViewById(R.id.VenuePageTitle);
        TextView upcoming = findViewById(R.id.venueUpcomingEvents);

        info.setText(venueInfo);
        venueName.setText(name);
        String upcomignText = "There are " + testArr.length() + " upcoming events.";
        upcoming.setText(upcomignText);
    }

    private void setAdapter(){
        recyclerAdapter adapter = new recyclerAdapter(testArr, getApplicationContext());
        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(getApplicationContext());
        eventsRecycler.setLayoutManager(layoutManager);
        eventsRecycler.setItemAnimator(new DefaultItemAnimator());
        eventsRecycler.setAdapter(adapter);
    }

    private JSONArray createTestArray() throws JSONException {
        JSONObject event1 = new JSONObject();
        event1.put("id", 1);
        event1.put("artist_name", "Taake and Kampfar\nNecrowretch");
        event1.put("date", "2022-01-11");
        event1.put("location", "Orto club");

        JSONObject event2 = new JSONObject();
        event2.put("id", 2);
        event2.put("artist_name", "Bryan Adams");
        event2.put("date", "2022-02-09");
        event2.put("location", "Arena Stozice");

        JSONObject event3 = new JSONObject();
        event3.put("id", 3);
        event3.put("artist_name", "Tarja");
        event3.put("date", "2022-04-08");
        event3.put("location", "Kino Siska");

        JSONArray array = new JSONArray();
        array.put(event1);
        array.put(event2);
        array.put(event3);

        return array;
    }

}