package com.example.empnewsapp;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ScienceFragment extends Fragment {
    String API = "2aa4dba4a1bc4af3ac562d782f3bc2f7";
    ArrayList<ModalClass> modalClassArrayList;
    Adapter adapter;
    String country = "us";
    private RecyclerView recyclerViewofScience;
    private String category = "science";

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.sciencefragment, null);
        recyclerViewofScience = v.findViewById(R.id.recyclerviewofscience);
        modalClassArrayList = new ArrayList<>();
        recyclerViewofScience.setLayoutManager(new LinearLayoutManager(getContext()));
        adapter = new Adapter(getContext(), modalClassArrayList);
        recyclerViewofScience.setAdapter(adapter);

        findNews();

        return v;
    }
    private void findNews(){
        APIUtilities.getApiInterface().getCategoryNews(country, category, 10, API).enqueue(new Callback<MainNews>() {
            @Override
            public void onResponse(Call<MainNews> call, Response<MainNews> response) {
                if (response.isSuccessful()){
                    modalClassArrayList.addAll(response.body().getArticles());
                    adapter.notifyDataSetChanged();
                }

            }

            @Override
            public void onFailure(Call<MainNews> call, Throwable t) {

            }
        });

    }
}
