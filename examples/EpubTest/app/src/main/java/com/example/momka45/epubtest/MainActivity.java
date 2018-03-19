package com.example.momka45.epubtest;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ScrollView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import nl.siegmann.epublib.domain.Book;
import nl.siegmann.epublib.domain.Resource;
import nl.siegmann.epublib.domain.Spine;
import nl.siegmann.epublib.epub.EpubReader;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    TextView text;
    TextView chptNum;
    ScrollView sc;
    Button nxtChp;
    Button prvChp;
    Book book;
    int cur_chapter = 0;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        text = (TextView) findViewById(R.id.text);
        chptNum = (TextView) findViewById(R.id.page_tw);
        nxtChp = (Button) findViewById(R.id.next_btn);
        prvChp = (Button) findViewById(R.id.prev_btn);
        sc = (ScrollView) findViewById(R.id.scrollView);
        nxtChp.setOnClickListener(this);
        prvChp.setOnClickListener(this);

        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("application/epub+zip");
        startActivityForResult(intent, 42);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(requestCode == 42 && resultCode == Activity.RESULT_OK) {
            Uri uri = data.getData();
            try {
                InputStream epubInputStream = getContentResolver().openInputStream(uri);
                book = (new EpubReader()).readEpub(epubInputStream);
                //Log.i("epublib", "Opened book");
                open_chapter(0);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void open_chapter(int chapter) {
        Spine spine = new Spine(book.getTableOfContents());
        if(chapter < 0 || chapter >= spine.size()) {
            chapter = 0;
        }
        String book_str = "";
        Resource res = spine.getSpineReferences().get(chapter).getResource();
        InputStream is = null;
        try {
            is = res.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String line;
            while ((line = br.readLine()) != null) {
                book_str += line;
            }
            //Log.i("epublib", book_str);
            text.setText(Html.fromHtml(book_str, new ImageGetter(), null));
            chptNum.setText((chapter + 1) + "/" + spine.size());
            cur_chapter = chapter;
            sc.scrollTo(0,0);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onClick(View view) {
        switch(view.getId()) {
            case R.id.next_btn:
                open_chapter(cur_chapter + 1);
                break;
            case R.id.prev_btn:
                open_chapter(cur_chapter - 1);
                break;
        }
    }
    private class ImageGetter implements Html.ImageGetter {
        public Drawable getDrawable(String source) {
            try {
                Resource r = book.getResources().getByHref(source);
                if(r == null) {
                    r = book.getResources().getByHref("OEBPS/" + source);
                }
                //Log.i("epublib", r.getHref());
                Bitmap bm = BitmapFactory.decodeByteArray(r.getData(), 0, r.getData().length);
                Drawable drawable = new BitmapDrawable(getResources(), bm);
                drawable.setBounds(0, 0, drawable.getIntrinsicWidth()*2, drawable.getIntrinsicHeight()*2);
                return drawable;
            } catch (IOException e) {
                e.printStackTrace();
            } catch (NullPointerException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
