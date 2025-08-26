--
-- Simplified PostgreSQL database dump with selected tables only
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';
SET default_table_access_method = heap;

--
-- Name: shareowner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shareowner (
    id integer,
    name text,
    shares integer
);

--
-- Name: animalowner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animalowner (
    animalname text,
    category text,
    owner_id integer
);

--
-- Name: shareowner1row; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shareowner1row (
    id integer,
    name text,
    shares integer
);

--
-- Name: animalowner1row; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animalowner1row (
    animalname text,
    category text,
    owner_id integer
);

--
-- Name: doctors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctors (
    id integer,
    name text,
    patients_pd text
);

--
-- Name: songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.songs (
    id integer,
    album_id integer,
    song_name text,
    duration text
);

--
-- Name: albums; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.albums (
    id integer,
    artist_id integer,
    album_name text,
    release_year integer
);

--
-- Name: artists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artists (
    id integer,
    name text,
    language text
);

--
-- Name: tennis_players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tennis_players (
    id integer,
    name text,
    born text
);

--
-- Name: tournaments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tournaments (
    id integer,
    name text,
    price text
);

--
-- Name: influencers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.influencers (
    media_name text,
    clicks text
);

--
-- Name: followers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.followers (
    id text,
    following text,
    adult boolean
);

--
-- Name: children_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.children_table (
    id text,
    children text
);

--
-- Name: fathers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fathers (
    id text,
    name text
);

--
-- Name: mothers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mothers (
    id text,
    name text
);

--
-- Name: website_visits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.website_visits (
    date text,
    page text,
    visits integer
);

--
-- Name: weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weather (
    date text,
    city text,
    temperature integer,
    rainfall integer
);

--
-- Name: bakery_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bakery_sales (
    item text,
    quantity text,
    price text
);

--
-- Name: oven_temperature; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oven_temperature (
    item text,
    temperature text
);

--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    movie text,
    category text,
    rating text
);

--
-- Name: clicks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clicks (
    publication text,
    clicks text
);

--
-- Name: movies_personal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies_personal (
    movie text,
    personal_rating text
);

--
-- Data for Name: shareowner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shareowner (id, name, shares) FROM stdin;
1	Pierre	20
2	Vladi	10
3	Diego	15
4	Marcel	11
\.

--
-- Data for Name: animalowner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.animalowner (animalname, category, owner_id) FROM stdin;
bill	chien	1
diego	chat	2
chris	dog	3
juan	perro	4
\.

--
-- Data for Name: shareowner1row; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shareowner1row (id, name, shares) FROM stdin;
1	Pierre	20
\.

--
-- Data for Name: animalowner1row; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.animalowner1row (animalname, category, owner_id) FROM stdin;
bill	chien	1
\.

--
-- Data for Name: doctors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctors (id, name, patients_pd) FROM stdin;
2	Giovanni	11
3	Hans	fourty
4	Lukas	44
1	Peter	ten
5	Dr. Smith	150
\.

--
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.songs (id, album_id, song_name, duration) FROM stdin;
1	1	Delicate	3:52
2	2	New Year's Day	3:55
\.

--
-- Data for Name: albums; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.albums (id, artist_id, album_name, release_year) FROM stdin;
1	1	Reputation	2017
2	2	Reputation	2017
\.

--
-- Data for Name: artists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artists (id, name, language) FROM stdin;
1	Taylor Swift	English
2	Reputation Artist	English
\.

--
-- Data for Name: tennis_players; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tennis_players (id, name, born) FROM stdin;
1	Juan	20.02.2003
2	Paul	18.04.1968
3	Xi	January 1986
4	Michael	18.01.1997
\.

--
-- Data for Name: tournaments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tournaments (id, name, price) FROM stdin;
4	Berlin Open	4
3	Warsaw Open	3
2	Jakarta Open	1.5
3	Osaka Open	0.5
\.

--
-- Data for Name: influencers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.influencers (media_name, clicks) FROM stdin;
makeuptutorial	1000 thousand
outsideguy	50
surviver1000	1 million
princess	one thousand
\.

--
-- Data for Name: followers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.followers (id, following, adult) FROM stdin;
1	surviver1000	t
3	makeuptutorial	f
2	surviver1000	t
3	princess	t
\.

--
-- Data for Name: children_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.children_table (id, children) FROM stdin;
0	4
1	1
2	many
3	2
\.

--
-- Data for Name: fathers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fathers (id, name) FROM stdin;
zero	Gerhard
one	Joachim
four	Simon
two	Dieter
\.

--
-- Data for Name: mothers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mothers (id, name) FROM stdin;
1	Julia
2	Petra
3	Claudia
4	Lena
\.

--
-- Data for Name: website_visits; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.website_visits (date, page, visits) FROM stdin;
2023 October 26	homepage	1000
2023 October 26	about	500
2023 October 27	homepage	1200
2023 October 27	contact	200
\.

--
-- Data for Name: weather; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weather (date, city, temperature, rainfall) FROM stdin;
2023 10 26	London	12	0
2023 10 26	New York	15	2
2023 10 27	London	10	5
2023 10 27	New York	13	1
\.

--
-- Data for Name: bakery_sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bakery_sales (item, quantity, price) FROM stdin;
Croissants	5 dozen	12.00 per dozen
Baguettes	8 dozen	10.00 per dozen
Macarons	7 dozen	12.00 per dozen
Pain au Chocolat	3 dozen	15.00 per dozen
\.

--
-- Data for Name: oven_temperature; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oven_temperature (item, temperature) FROM stdin;
Croissants	200 °F
Baguettes	400 °F
Macarons	350 °F
Pain au Chocolat	200 °F
\.

--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (movie, category, rating) FROM stdin;
Raiders of the Lost Arc	action	4/5
The Shawshank Redemption	thriller	3/5
Wings of Desire	fantasy	4/5
Amélie	comedy	5/5
\.

--
-- Data for Name: clicks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clicks (publication, clicks) FROM stdin;
17.01.2011	1000000
08.03.2016	500
22.11.2014	10^6
24.12.2022	1000
\.

--
-- Data for Name: movies_personal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies_personal (movie, personal_rating) FROM stdin;
Die Flucht aus Shawshank	3/5
Der Himmel über Berlin	5/5
Die fabelhafte Welt der Amélie	4/5
Lola rennt	2/5
\.

--
-- PostgreSQL database dump complete
--
