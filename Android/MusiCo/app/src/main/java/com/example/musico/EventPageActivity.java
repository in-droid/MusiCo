package com.example.musico;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.JsonReader;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Array;
import java.net.MalformedURLException;
import java.net.URL;

public class EventPageActivity extends AppCompatActivity {
    private JSONObject testObj;

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event_page);

        Button backBtn = findViewById(R.id.backBtn);
        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getApplicationContext(), AllEventsActivity.class);
                startActivity(i);
            }
        });

        //TextView eventID = findViewById(R.id.eventID);
        //int id = Integer.parseInt((String) getIntent().getSerializableExtra("eventID"));
        //eventID.setText(String.format("%d", id));

        try {
            testObj = createTestObj();
        } catch (JSONException e) {
            e.printStackTrace();
        }

        TextView artistName = findViewById(R.id.name);
        TextView location = findViewById(R.id.locationTitle);
        TextView date = findViewById(R.id.dateTitle);
        TextView lineup = findViewById(R.id.lineupBody);
        TextView venueInfo = findViewById(R.id.venueInfoBody);
        TextView addInfo = findViewById(R.id.addInfoBody);
        ImageView artistImg = findViewById(R.id.artistImg);
        Button ticketBtn = findViewById(R.id.ticketBtn);

        TextView lineupTitle = findViewById(R.id.lineupTitle);
        TextView ticketsTitle = findViewById(R.id.ticketTitle);
        TextView addInfoTitle = findViewById(R.id.addInfoTitle);
        Button venuePage = findViewById(R.id.toVenuePageBtn);
        try {
            artistName.setText(testObj.getJSONObject("artist").getString("name"));
            String locationFull = testObj.getJSONObject("venue").getString("name") + ", " +
                    testObj.getString("city") + ", " + testObj.getString("country");
            location.setText(locationFull);
            date.setText(testObj.getString("date"));

            try {
                String lineupStr = testObj.getString("lineup");
                lineupStr = lineupStr.substring(1,lineupStr.length()-1);
                lineupStr = lineupStr.replaceAll("'","");
                lineup.setText(lineupStr);
            }
            catch (Exception e){
                lineup.setVisibility(View.GONE);
                lineupTitle.setVisibility(View.GONE);
            }

            venueInfo.setText(testObj.getJSONObject("venue").getString("venue_info"));

            try {
                String addInfoText = testObj.getString("additional_info");
                addInfo.setText(addInfoText);
            }
            catch (Exception e){
                addInfo.setVisibility(View.GONE);
                addInfoTitle.setVisibility(View.GONE);
            }

            //go to ticket page
            try {
                String ticketUrl = testObj.getString("tickets");
                ticketBtn.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent browserIntent = null;
                        browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(ticketUrl));
                        startActivity(browserIntent);
                    }
                });
            }
            catch (Exception e){
                ticketBtn.setVisibility(View.GONE);
                ticketsTitle.setText("Tickets are not available");
            }

            //show image
            try {
                String imgUrl = testObj.getJSONObject("artist").getString("img_link");
                Picasso.get().load(imgUrl).into(artistImg);
            }
            catch (Exception e){
                artistImg.setVisibility(View.GONE);
            }

            //initialize toVenuePage button
            venuePage.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(getApplicationContext(), VenuePageActivity.class);
                    try {
                        intent.putExtra("venueID", testObj.getJSONObject("venue").getString("id"));
                        intent.putExtra("venueName", testObj.getJSONObject("venue").getString("name"));
                        intent.putExtra("venueInfo", testObj.getJSONObject("venue").getString("venue_info"));
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    startActivity(intent);
                }
            });

        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private JSONObject createTestObj() throws JSONException {
        JSONObject artist = new JSONObject();
        artist.put("id", 1);
        artist.put("name", "Taake and Kampfar\nNecrowretch");
        artist.put("img_link", "https://images.sk-static.com/images/media/profile_images/artists/2915/huge_avatar");

        JSONObject venue = new JSONObject();
        venue.put("id", 1);
        venue.put("name", "Orto");
        venue.put("venue_info", "Grablovicceva 1\n" +
                "1000\n" +
                "Ljubljana, Slovenia");

        JSONObject event = new JSONObject();
        event.put("id", 1);
        event.put("artist", artist);
        event.put("date", "2022-01-11");
        event.put("venue", venue);
        event.put("lineup", "['Taake', 'Kampfar', 'Necrowretch']");
        event.put("city", "Ljubljana");
        event.put("country", "Slovenia");
        event.put("additional_info", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
        event.put("tickets", "https://www.songkick.com/tickets/29829402?");

        return event;
    }

}