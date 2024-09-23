from tkinter import *
from PIL import ImageTk, Image
import requests
import json
from io import BytesIO
import threading


class Window:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x600")
        self.master.configure(bg="#2D2727")
        self.home()

    def home(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.home_taskbar = LabelFrame(
            self.master,
            bg="#413543",
            height=500,
            width=100,
            highlightthickness=0,
            borderwidth=0,
        )
        self.home_taskbar.pack(side="left", fill="y")

        self.img_logo = Image.open("logo.png")
        self.img_logo = self.img_logo.resize((90, 90))
        self.img_logo = ImageTk.PhotoImage(self.img_logo)
        self.home_button = Button(
            self.home_taskbar, image=self.img_logo, command=self.home
        )
        self.home_button.place(x=0, y=1)

        self.movie_logo = Image.open("movie_logo.png")
        self.movie_logo = self.movie_logo.resize((35, 35))
        self.movie_logo = ImageTk.PhotoImage(self.movie_logo)
        self.movies_button = Button(
            self.home_taskbar,
            highlightthickness=0,
            borderwidth=0,
            image=self.movie_logo,
            command=self.movies,
        )
        self.movies_button.place(x=25, y=125)

        self.tv_shows_logo = Image.open("tv_show_logo.png")
        self.tv_shows_logo = self.tv_shows_logo.resize((35, 35))
        self.tv_shows_logo = ImageTk.PhotoImage(self.tv_shows_logo)
        self.tv_shows = Button(
            self.home_taskbar,
            image=self.tv_shows_logo,
            highlightthickness=0,
            borderwidth=0,
            command=self.tv,
        )
        self.tv_shows.place(x=25, y=210)

        self.movie_search = Entry(self.master, width=44)
        self.movie_search.insert(0, " Enter keywords... ")
        self.movie_search.place(x=200, y=20)

        self.movie_search_logo = Image.open("search.png")
        self.movie_search_logo = self.movie_search_logo.resize((25, 21))
        self.movie_search_logo = ImageTk.PhotoImage(self.movie_search_logo)
        self.movie_search_button = Button(
            self.master,
            image=self.movie_search_logo,
            highlightthickness=0,
            borderwidth=0,
            command=self.search,
        )
        self.movie_search_button.place(x=600, y=22)

    def search(self):
        threading.Thread(target=self._search).start()

    def _search(self):
        self._show_loading()  # Show loading feedback

        title = self.movie_search.get()
        api_key = "*"

        # Check cache for search_response
        if title in self.cache_search:
            search_response = self.cache_search[title]
        else:
            search_response = requests.get(
                f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
            ).json()
            self.cache_search[title] = search_response

        movie_id = search_response["results"][0]["id"]

        # Check cache for similar_response
        if movie_id in self.cache_similar:
            similar_response = self.cache_similar[movie_id]
        else:
            similar_response = requests.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={api_key}&language=en-US&page=1"
            ).json()
            self.cache_similar[movie_id] = similar_response

        movie_list = []
        poster_list = []

        for i in similar_response["results"]:
            movie_list.append(i["id"])
            poster_list.append(i["poster_path"])
            if len(movie_list) and len(poster_list) == 10:
                break

        # Update UI
        self.master.after(0, lambda: self._show_posters(movie_list, poster_list))
        self._hide_loading()  # Hide loading feedback

    def _show_loading(self):
        # create and display a loading label
        self.loading_label = Label(self.master, text="Loading...", bg="#2D2727")
        self.loading_label.place(x=400, y=90)

    def _hide_loading(self):
        self.loading_label.destroy()

    def _show_posters(self, movie_list, poster_list):
        if hasattr(self, "poster_frame"):
            self.poster_frame.destroy()

        self.poster_frame = Frame(self.master, bg="#2D2727")
        self.poster_frame.place(x=150, y=100)

        for idx, poster_path in enumerate(poster_list):
            # Check cache for poster
            if poster_path in self.cache_poster:
                poster_image = self.cache_poster[poster_path]
            else:
                response = requests.get(
                    f"https://image.tmdb.org/t/p/original/{poster_path}"
                )
                poster = Image.open(BytesIO(response.content))
                poster = poster.resize((150, 150))
                poster_image = ImageTk.PhotoImage(poster)
                self.cache_poster[poster_path] = poster_image  # Cache the image

            poster_label = Label(self.poster_frame, image=poster_image, bg="#2D2727")
            poster_label.image = poster_image
            poster_label.grid(row=idx // 5, column=idx % 5, padx=10, pady=10)

    cache_search = {}
    cache_similar = {}
    cache_poster = {}

    def movies(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.home_taskbar1 = LabelFrame(
            self.master,
            bg="#413543",
            height=500,
            width=100,
            highlightthickness=0,
            borderwidth=0,
        )
        self.home_taskbar1.pack(side="left", fill="y")

        self.img_logo1 = Image.open("logo.png")
        self.img_logo1 = self.img_logo1.resize((90, 90))
        self.img_logo1 = ImageTk.PhotoImage(self.img_logo1)
        self.home_button1 = Button(
            self.home_taskbar1, image=self.img_logo1, command=self.home
        )
        self.home_button1.place(x=0, y=1)

        self.movie_logo1 = Image.open("movie_logo_selected.png")
        self.movie_logo1 = self.movie_logo1.resize((35, 35))
        self.movie_logo1 = ImageTk.PhotoImage(self.movie_logo1)
        self.movies_button1 = Button(
            self.home_taskbar1,
            highlightthickness=0,
            borderwidth=0,
            image=self.movie_logo1,
        )
        self.movies_button1.place(x=25, y=125)

        self.tv_shows_logo1 = Image.open("tv_show_logo.png")
        self.tv_shows_logo1 = self.tv_shows_logo1.resize((35, 35))
        self.tv_shows_logo1 = ImageTk.PhotoImage(self.tv_shows_logo1)
        self.tv_shows1 = Button(
            self.home_taskbar1,
            image=self.tv_shows_logo1,
            highlightthickness=0,
            borderwidth=0,
            command=self.tv,
        )
        self.tv_shows1.place(x=25, y=210)
        # filtering

        self.genre_menubutton = Menubutton(
            self.master,
            text="Choose Genre",
            indicatoron=True,
            borderwidth=1,
            relief="raised",
            bg="#413543",
        )
        self.genre_menu = Menu(self.genre_menubutton, tearoff=False)
        self.genre_menubutton.configure(menu=self.genre_menu)
        self.genre_menubutton.place(x=250, y=25)

        self.genre_choices = {}
        for genre in (
            "Action",
            "Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "History",
            "Horror",
            "Music",
            "Mystery",
            "Romance",
            "Science Fiction",
            "Thriller",
            "TV Movie",
            "War",
            "Western",
        ):
            self.genre_choices[genre] = IntVar(value=0)
            self.genre_menu.add_checkbutton(
                label=genre,
                variable=self.genre_choices[genre],
                onvalue=1,
                offvalue=0,
                command=self.storeSelectedGenres,
            )
        self.selected_genre = []
        self.genre_ids = {
            "Action": 28,
            "Adventure": 12,
            "Animation": 16,
            "Comedy": 35,
            "Crime": 80,
            "Documentary": 99,
            "Drama": 18,
            "Family": 10751,
            "Fantasy": 14,
            "History": 36,
            "Horror": 27,
            "Music": 10402,
            "Mystery": 9648,
            "Romance": 10749,
            "Science Fiction": 878,
            "TV Movie": 10770,
            "Thriller": 53,
            "War": 10752,
            "Western": 37,
        }

        self.movie_filtering = Button(
            self.master,
            text="Apply Filters",
            width=10,
            height=2,
            command=self.search_movies,
        )
        self.movie_filtering.place(x=250, y=60)

        self.load_more_button = Button(
            self.master, text="Load More", command=self.load_more_movies
        )
        self.load_more_button.place(x=300, y=550)

        self.current_page = 1

    def load_more_movies(self):
        self.current_page += 1
        self._search_movies()

    def storeSelectedGenres(self):
        self.selected_genre.clear()
        for genre, var in self.genre_choices.items():
            if var.get():
                self.selected_genre.append(self.genre_ids[genre])

    def search_movies(self):
        threading.Thread(target=self._search_movies).start()

    def _show_posters(self, movie_list, poster_list):
        if hasattr(self, "poster_frame"):
            self.poster_frame.destroy()

        self.poster_frame = Frame(self.master, bg="#2D2727")
        self.poster_frame.place(x=150, y=100)

        row, column = 0, 0
        for idx, poster_path in enumerate(poster_list):
            # Check cache for poster
            if poster_path not in self.cache_poster:
                response = requests.get(
                    f"https://image.tmdb.org/t/p/original/{poster_path}"
                )
                poster = Image.open(BytesIO(response.content))
                poster = poster.resize((150, 150))
                poster_image = ImageTk.PhotoImage(poster)
                self.cache_poster[poster_path] = poster_image  # Cache the image

            poster_label = Label(
                self.poster_frame, image=self.cache_poster[poster_path], bg="#2D2727"
            )
            poster_label.image = self.cache_poster[poster_path]
            poster_label.grid(row=row, column=column, padx=10, pady=10)
            column += 1
            if column == 5:
                row += 1
                column = 0

    def _search_movies(self):
        api_key = "*"
        self._show_loading()

        self.storeSelectedGenres()

        search_response_movie = requests.get(
            f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={','.join(map(str, self.selected_genre))}&page={self.current_page}"
        ).json()
        movie_list1 = []
        poster_list1 = []

        for c in search_response_movie["results"]:
            movie_list1.append(c["id"])
            poster_list1.append(c["poster_path"])
            if len(movie_list1) and len(poster_list1) == 10:
                break

        self.master.after(0, lambda: self._show_posters(movie_list1, poster_list1))
        self._hide_loading()

    def tv(self):
        for i in self.master.winfo_children():
            i.destroy()

        self.home_taskbar2 = LabelFrame(
            self.master,
            bg="#413543",
            height=500,
            width=100,
            highlightthickness=0,
            borderwidth=0,
        )
        self.home_taskbar2.pack(side="left", fill="y")

        self.img_logo2 = Image.open("logo.png")
        self.img_logo2 = self.img_logo2.resize((90, 90))
        self.img_logo2 = ImageTk.PhotoImage(self.img_logo2)
        self.home_button2 = Button(
            self.home_taskbar2, image=self.img_logo2, command=self.home
        )
        self.home_button2.place(x=0, y=1)

        self.movie_logo2 = Image.open("movie_logo.png")
        self.movie_logo2 = self.movie_logo2.resize((35, 35))
        self.movie_logo2 = ImageTk.PhotoImage(self.movie_logo2)
        self.movies_button2 = Button(
            self.home_taskbar2,
            highlightthickness=0,
            borderwidth=0,
            image=self.movie_logo2,
            command=self.movies,
        )
        self.movies_button2.place(x=25, y=125)

        self.tv_shows_logo2 = Image.open("tv_show_logo_selected.png")
        self.tv_shows_logo2 = self.tv_shows_logo2.resize((35, 35))
        self.tv_shows_logo2 = ImageTk.PhotoImage(self.tv_shows_logo2)
        self.tv_shows2 = Button(
            self.home_taskbar2,
            image=self.tv_shows_logo2,
            highlightthickness=0,
            borderwidth=0,
            command=self.tv,
        )
        self.tv_shows2.place(x=25, y=210)

    def tv(self):
        for i in self.master.winfo_children():
            i.destroy()
    
        self.home_taskbar2 = LabelFrame(
        self.master,
        bg="#413543",
        height=500,
        width=100,
        highlightthickness=0,
        borderwidth=0,
    )
        self.home_taskbar2.pack(side="left", fill="y")
    
        self.img_logo2 = Image.open("logo.png")
        self.img_logo2 = self.img_logo2.resize((90, 90))
        self.img_logo2 = ImageTk.PhotoImage(self.img_logo2)
        self.home_button2 = Button(
            self.home_taskbar2, image=self.img_logo2, command=self.home
        )
        self.home_button2.place(x=0, y=1)
        
        self.movie_logo2 = Image.open("movie_logo.png")
        self.movie_logo2 = self.movie_logo2.resize((35, 35))
        self.movie_logo2 = ImageTk.PhotoImage(self.movie_logo2)
        self.movies_button2 = Button(
            self.home_taskbar2,
            highlightthickness=0,
            borderwidth=0,
            image=self.movie_logo2,
            command=self.movies,
        )
        self.movies_button2.place(x=25, y=125)
        
        self.tv_shows_logo2 = Image.open("tv_show_logo_selected.png")
        self.tv_shows_logo2 = self.tv_shows_logo2.resize((35, 35))
        self.tv_shows_logo2 = ImageTk.PhotoImage(self.tv_shows_logo2)
        self.tv_shows2 = Button(
            self.home_taskbar2,
            image=self.tv_shows_logo2,
            highlightthickness=0,
            borderwidth=0,
        )
        self.tv_shows2.place(x=25, y=210)
        
        # filtering
        self.genre_menubutton = Menubutton(
            self.master,
            text="Choose Genre",
            indicatoron=True,
            borderwidth=1,
            relief="raised",
            bg="#413543",
        )
        self.genre_menu = Menu(self.genre_menubutton, tearoff=False)
        self.genre_menubutton.configure(menu=self.genre_menu)
        self.genre_menubutton.place(x=250, y=25)
        
        self.genre_choices = {}
        for genre in (
            "Action & Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Kids",
            "Mystery",
            "News",
            "Reality",
            "Sci-Fi & Fantasy",
            "Soap",
            "Talk",
            "War & Politics",
            "Western",
        ):
            self.genre_choices[genre] = IntVar(value=0)
            self.genre_menu.add_checkbutton(
                label=genre,
                variable=self.genre_choices[genre],
                onvalue=1,
                offvalue=0,
                command=self.TvStoreSelectedGenres,
            )
        self.selected_genre = []
        self.genre_ids = {
            "Action & Adventure": 10759,
            "Animation": 16,
            "Comedy": 35,
            "Crime": 80,
            "Documentary": 99,
            "Drama": 18,
            "Family": 10751,
            "Kids": 10762,
            "Mystery": 9648,
            "News": 10763,
            "Reality": 10764,
            "Sci-Fi & Fantasy": 10765,
            "Soap": 10766,
            "Talk": 10767,
            "War & Politics": 10768,
            "Western": 37,
        }
        
        self.tv_filtering = Button(
            self.master,
            text="Apply Filters",
            width=10,
            height=2,
            command=self.search_tv_shows,
        )
        self.tv_filtering.place(x=250, y=60)
        
        self.load_more_button = Button(
            self.master, text="Load More", command=self.load_more_tv_shows
        )
        self.load_more_button.place(x=300, y=550)
        
        self.current_page = 1

    def load_more_tv_shows(self):
        self.current_page += 1
        self._search_tv_shows()

    def TvStoreSelectedGenres(self):
        self.selected_genre.clear()
        for genre, var in self.genre_choices.items():
            if var.get():
                self.selected_genre.append(self.genre_ids[genre])

    def search_tv_shows(self):
        threading.Thread(target=self._search_tv_shows).start()

    def _search_tv_shows(self):
        api_key = "*"
        self._show_loading()
        
        self.TvStoreSelectedGenres()
        
        search_response_tv = requests.get(
            f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&with_genres={','.join(map(str, self.selected_genre))}&page={self.current_page}"
        ).json()
        tv_list = []
        poster_list = []
        
        for c in search_response_tv["results"]:
            tv_list.append(c["id"])
            poster_list.append(c["poster_path"])
            if len(tv_list) and len(poster_list) == 10:
                break
        
        self.master.after(0, lambda: self._show_posters(tv_list, poster_list))
        self._hide_loading()

root = Tk()
Window(root)
root.mainloop()
