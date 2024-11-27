--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 17.0 (Ubuntu 17.0-1.pgdg22.04+1)

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

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: albums; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.albums (
    id integer NOT NULL,
    artist_id integer,
    album_name text,
    release_year text
);


ALTER TABLE public.albums OWNER TO postgres;

--
-- Name: animalowner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animalowner (
    owner_id integer NOT NULL,
    animalname text,
    category text
);


ALTER TABLE public.animalowner OWNER TO postgres;

--
-- Name: artists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artists (
    id integer NOT NULL,
    name text,
    language text
);


ALTER TABLE public.artists OWNER TO postgres;

--
-- Name: shareowner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shareowner (
    id integer NOT NULL,
    name text,
    shares integer
);


ALTER TABLE public.shareowner OWNER TO postgres;

--
-- Name: songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.songs (
    id integer NOT NULL,
    album_id integer,
    song_name text,
    duration text
);


ALTER TABLE public.songs OWNER TO postgres;

--
-- Name: totalanimal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.totalanimal (
    name text NOT NULL,
    category text
);


ALTER TABLE public.totalanimal OWNER TO postgres;

--
-- Name: totalnation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.totalnation (
    id text NOT NULL,
    nationality text
);


ALTER TABLE public.totalnation OWNER TO postgres;

--
-- Name: totalshares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.totalshares (
    name text NOT NULL,
    shares integer
);


ALTER TABLE public.totalshares OWNER TO postgres;

--
-- Data for Name: albums; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.albums (id, artist_id, album_name, release_year) FROM stdin;
1	1	Reputation	2017
2	2	Reputation	2017
\.


--
-- Data for Name: animalowner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.animalowner (owner_id, animalname, category) FROM stdin;
1	bill	chien
2	diego	chat
3	chris	dog
4	juan	perro
\.


--
-- Data for Name: artists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artists (id, name, language) FROM stdin;
1	Taylor Swift	English
2	Reputation Artist	English
\.


--
-- Data for Name: shareowner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shareowner (id, name, shares) FROM stdin;
1	Pierre\n	20
2	Vladi\n	10
3	Diego	15
4	Marcel	11
\.


--
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.songs (id, album_id, song_name, duration) FROM stdin;
1	1	Delicate	3:52
2	2	New Year’s Day	3:55
\.


--
-- Data for Name: totalanimal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.totalanimal (name, category) FROM stdin;
bill	chien
diego	chat
\.


--
-- Data for Name: totalnation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.totalnation (id, nationality) FROM stdin;
Vladi	Germany
\.


--
-- Data for Name: totalshares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.totalshares (name, shares) FROM stdin;
Felix	20
Vladi	10
Peter	9
Max	9
\.


--
-- Name: albums album_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT album_pkey PRIMARY KEY (id);


--
-- Name: animalowner animalowner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animalowner
    ADD CONSTRAINT animalowner_pkey PRIMARY KEY (owner_id);


--
-- Name: artists artists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artists
    ADD CONSTRAINT artists_pkey PRIMARY KEY (id);


--
-- Name: shareowner shareowner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shareowner
    ADD CONSTRAINT shareowner_pkey PRIMARY KEY (id);


--
-- Name: totalshares shares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.totalshares
    ADD CONSTRAINT shares_pkey PRIMARY KEY (name);


--
-- Name: songs songs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs
    ADD CONSTRAINT songs_pkey PRIMARY KEY (id);


--
-- Name: totalanimal totalanimal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.totalanimal
    ADD CONSTRAINT totalanimal_pkey PRIMARY KEY (name);


--
-- Name: totalnation totalnation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.totalnation
    ADD CONSTRAINT totalnation_pkey PRIMARY KEY (id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

