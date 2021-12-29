package com.example.empnewsapp;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

public class PagerAdapter extends FragmentPagerAdapter {


    int tab_count;

    public PagerAdapter(@NonNull FragmentManager fm, int behavior) {
        super(fm, behavior);
        tab_count = behavior;
    }

    @NonNull
    @Override
    public Fragment getItem(int position) {
        switch (position) {
            case 0:
                return new HomeFragment();
            case 1:
                return new SportFragment();
            case 2:
                return new HealthFragment();
            case 3:
                return new ScienceFragment();
            case 4:
                return new EntertainementFragment();
            case 5:
                return new TechnologyFragment();
            default:
                return null;
        }
    }

    @Override
    public int getCount() {
        return tab_count;
    }
}
