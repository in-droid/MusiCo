package com.example.musico;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.textfield.TextInputEditText;

import org.json.JSONArray;
import org.json.JSONException;

public class recyclerAdapter extends RecyclerView.Adapter<recyclerAdapter.myViewHolder> {

    private JSONArray eventList;
    private Context appContext;

    public recyclerAdapter(JSONArray eventList, Context context){
        this.eventList = eventList;
        this.appContext = context;
    }

    public class myViewHolder extends RecyclerView.ViewHolder{
        private TextView nameTxt;
        private TextView locationTxt;
        private TextView dateTxt;
        private Button toEventBtn;

        public myViewHolder(final View view){
            super(view);
            nameTxt = view.findViewById(R.id.EventName);
            locationTxt = view.findViewById(R.id.location);
            dateTxt = view.findViewById(R.id.date);
            toEventBtn = view.findViewById(R.id.toEventPageBtn);
        }
    }

    @NonNull
    @Override
    public recyclerAdapter.myViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View eventView = LayoutInflater.from(parent.getContext()).inflate(R.layout.content_all_events, parent, false);
        return new myViewHolder(eventView);
    }

    @Override
    public void onBindViewHolder(@NonNull recyclerAdapter.myViewHolder holder, int position) {
        try {
            String eventName = eventList.getJSONObject(position).getString("artist_name");
            String location = eventList.getJSONObject(position).getString("location");
            String date = eventList.getJSONObject(position).getString("date");
            int eventID = eventList.getJSONObject(position).getInt("id");

            holder.nameTxt.setText(eventName);
            holder.locationTxt.setText(location);
            holder.dateTxt.setText(date);
            holder.toEventBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(appContext, EventPageActivity.class);
                    intent.putExtra("eventID", eventID);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_MULTIPLE_TASK);
                    appContext.startActivity(intent);
                }
            });

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int getItemCount() {
        return eventList.length();
    }
}
