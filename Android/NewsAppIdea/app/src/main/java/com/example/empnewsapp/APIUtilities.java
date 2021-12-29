package com.example.empnewsapp;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class APIUtilities {

    private static Retrofit retrofit = null;

    public static APIInterface getApiInterface(){
        if (retrofit == null){
            retrofit = new Retrofit.Builder().baseUrl(APIInterface.BASE_URL).addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit.create(APIInterface.class);
    }
}
