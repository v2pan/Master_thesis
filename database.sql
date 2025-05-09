--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Ubuntu 17.2-1.pgdg22.04+1)
-- Dumped by pg_dump version 17.2 (Ubuntu 17.2-1.pgdg22.04+1)

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

--
-- Name: plpython3u; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpython3u WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpython3u; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpython3u IS 'PL/Python3U untrusted procedural language';


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


--
-- Name: normalize_category(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.normalize_category(category text) RETURNS text
    LANGUAGE plpython3u
    AS $$
# Define a set of terms that mean "dog" in different languages
dog_terms = {'dog', 'chien', 'perro', 'Hund', 'cane'}
if category in dog_terms:
    return 'dog'
return category
$$;


ALTER FUNCTION public.normalize_category(category text) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: airport; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.airport (
    airportname text,
    city text
);


ALTER TABLE public.airport OWNER TO postgres;

--
-- Name: airport_abrev; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.airport_abrev (
    name text
);


ALTER TABLE public.airport_abrev OWNER TO postgres;

--
-- Name: airport_transl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.airport_transl (
    fullname text,
    shortname text
);


ALTER TABLE public.airport_transl OWNER TO postgres;

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
-- Name: animalowner1row; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animalowner1row (
    owner_id integer NOT NULL,
    animalname text,
    category text
);


ALTER TABLE public.animalowner1row OWNER TO postgres;

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
-- Name: bakery_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bakery_sales (
    item text,
    quantity text,
    price text
);


ALTER TABLE public.bakery_sales OWNER TO postgres;

--
-- Name: bakery_salesitemoven_temperatureitem_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bakery_salesitemoven_temperatureitem_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.bakery_salesitemoven_temperatureitem_table OWNER TO postgres;

--
-- Name: chemical; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chemical (
    name text NOT NULL,
    melting_point real
);


ALTER TABLE public.chemical OWNER TO postgres;

--
-- Name: chemical_abrev; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chemical_abrev (
    name_abrev text
);


ALTER TABLE public.chemical_abrev OWNER TO postgres;

--
-- Name: chemical_translations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chemical_translations (
    full_name text,
    short_name text
);


ALTER TABLE public.chemical_translations OWNER TO postgres;

--
-- Name: children_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.children_table (
    id integer,
    children character varying(255)
);


ALTER TABLE public.children_table OWNER TO postgres;

--
-- Name: children_tableidfathersid_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.children_tableidfathersid_table (
    word integer NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.children_tableidfathersid_table OWNER TO postgres;

--
-- Name: doctors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctors (
    id integer NOT NULL,
    name text,
    patients_pd text
);


ALTER TABLE public.doctors OWNER TO postgres;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    content text,
    embedding public.vector(768)
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: fathers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fathers (
    id character varying(255),
    name character varying(255)
);


ALTER TABLE public.fathers OWNER TO postgres;

--
-- Name: followers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.followers (
    id integer,
    media_name text,
    adult boolean
);


ALTER TABLE public.followers OWNER TO postgres;

--
-- Name: influencers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.influencers (
    media_name text NOT NULL,
    clicks text
);


ALTER TABLE public.influencers OWNER TO postgres;

--
-- Name: influencersclickspublication_clicksclicks_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.influencersclickspublication_clicksclicks_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.influencersclickspublication_clicksclicks_table OWNER TO postgres;

--
-- Name: influencersmedia_namefollowersmedia_name_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.influencersmedia_namefollowersmedia_name_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.influencersmedia_namefollowersmedia_name_table OWNER TO postgres;

--
-- Name: mothers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mothers (
    id integer,
    name character varying(255)
);


ALTER TABLE public.mothers OWNER TO postgres;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    movie text NOT NULL,
    category text,
    rating text
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- Name: movies_personal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies_personal (
    movie text NOT NULL,
    personal_rating text
);


ALTER TABLE public.movies_personal OWNER TO postgres;

--
-- Name: moviesmoviemovies_personalmovie_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.moviesmoviemovies_personalmovie_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.moviesmoviemovies_personalmovie_table OWNER TO postgres;

--
-- Name: oven_temperature; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oven_temperature (
    item text,
    temperature text
);


ALTER TABLE public.oven_temperature OWNER TO postgres;

--
-- Name: players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.players (
    id integer NOT NULL,
    name text,
    born text
);


ALTER TABLE public.players OWNER TO postgres;

--
-- Name: publication_clicks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_clicks (
    publication text,
    clicks text
);


ALTER TABLE public.publication_clicks OWNER TO postgres;

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
-- Name: shareowner1row; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shareowner1row (
    id integer NOT NULL,
    name text,
    shares integer
);


ALTER TABLE public.shareowner1row OWNER TO postgres;

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
-- Name: state_capitol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.state_capitol (
    name text,
    capitol text
);


ALTER TABLE public.state_capitol OWNER TO postgres;

--
-- Name: state_capitol_short; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.state_capitol_short (
    name text,
    capitol text
);


ALTER TABLE public.state_capitol_short OWNER TO postgres;

--
-- Name: state_trans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.state_trans (
    state_abrev text,
    state text
);


ALTER TABLE public.state_trans OWNER TO postgres;

--
-- Name: state_trans_short; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.state_trans_short (
    state_abrev text,
    state text
);


ALTER TABLE public.state_trans_short OWNER TO postgres;

--
-- Name: states; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.states (
    name text,
    population integer
);


ALTER TABLE public.states OWNER TO postgres;

--
-- Name: states_short; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.states_short (
    name text,
    population text
);


ALTER TABLE public.states_short OWNER TO postgres;

--
-- Name: tennis_players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tennis_players (
    id integer NOT NULL,
    name character varying(255),
    born character varying(255)
);


ALTER TABLE public.tennis_players OWNER TO postgres;

--
-- Name: totalanimal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.totalanimal (
    name text NOT NULL,
    category text
);


ALTER TABLE public.totalanimal OWNER TO postgres;

--
-- Name: totalshares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.totalshares (
    name text NOT NULL,
    shares integer
);


ALTER TABLE public.totalshares OWNER TO postgres;

--
-- Name: tournaments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tournaments (
    winner_id integer,
    name character varying(255),
    price_money_in_million double precision
);


ALTER TABLE public.tournaments OWNER TO postgres;

--
-- Name: translation_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.translation_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.translation_table OWNER TO postgres;

--
-- Name: weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weather (
    date character varying(255),
    city character varying(255),
    temperature integer,
    rainfall integer
);


ALTER TABLE public.weather OWNER TO postgres;

--
-- Name: weatherdatewebsite_visitsdate_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weatherdatewebsite_visitsdate_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.weatherdatewebsite_visitsdate_table OWNER TO postgres;

--
-- Name: website_visits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.website_visits (
    date character varying(255),
    page character varying(255),
    visits integer
);


ALTER TABLE public.website_visits OWNER TO postgres;

--
-- Name: whereanimalownercategorydog_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.whereanimalownercategorydog_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.whereanimalownercategorydog_table OWNER TO postgres;

--
-- Name: whereanimalownercategorydogoranimalownercategoryisnull_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.whereanimalownercategorydogoranimalownercategoryisnull_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.whereanimalownercategorydogoranimalownercategoryisnull_table OWNER TO postgres;

--
-- Name: whereanimalownercategoryisnulloranimalownercategorydog_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.whereanimalownercategoryisnulloranimalownercategorydog_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.whereanimalownercategoryisnulloranimalownercategorydog_table OWNER TO postgres;

--
-- Name: wherebakery_salesquantity55_comparison_55_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wherebakery_salesquantity55_comparison_55_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wherebakery_salesquantity55_comparison_55_table OWNER TO postgres;

--
-- Name: wherechildren_tablechildren1_comparison_1_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wherechildren_tablechildren1_comparison_1_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wherechildren_tablechildren1_comparison_1_table OWNER TO postgres;

--
-- Name: wheredoctorsnamepeteranddoctorspatients_pd12_comparison_12_tabl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wheredoctorsnamepeteranddoctorspatients_pd12_comparison_12_tabl (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wheredoctorsnamepeteranddoctorspatients_pd12_comparison_12_tabl OWNER TO postgres;

--
-- Name: wheredoctorsnamepeteranddoctorspatients_pd12_comparison_peter_t; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wheredoctorsnamepeteranddoctorspatients_pd12_comparison_peter_t (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wheredoctorsnamepeteranddoctorspatients_pd12_comparison_peter_t OWNER TO postgres;

--
-- Name: wheredoctorsnamepeteranddoctorspatients_pd12_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wheredoctorsnamepeteranddoctorspatients_pd12_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wheredoctorsnamepeteranddoctorspatients_pd12_table OWNER TO postgres;

--
-- Name: wheredoctorspatients_pd12_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wheredoctorspatients_pd12_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wheredoctorspatients_pd12_table OWNER TO postgres;

--
-- Name: whereinfluencersclicks500_comparison_500_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.whereinfluencersclicks500_comparison_500_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.whereinfluencersclicks500_comparison_500_table OWNER TO postgres;

--
-- Name: wheremovies_personalpersonal_rating70_comparison_70_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wheremovies_personalpersonal_rating70_comparison_70_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wheremovies_personalpersonal_rating70_comparison_70_table OWNER TO postgres;

--
-- Name: whereoven_temperaturetemperature200°c_comparison_200°c_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."whereoven_temperaturetemperature200°c_comparison_200°c_table" (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public."whereoven_temperaturetemperature200°c_comparison_200°c_table" OWNER TO postgres;

--
-- Name: wheretennis_playersbornjanuary_comparison_january_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wheretennis_playersbornjanuary_comparison_january_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wheretennis_playersbornjanuary_comparison_january_table OWNER TO postgres;

--
-- Data for Name: airport; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.airport (airportname, city) FROM stdin;
Denver International Airport	Denver
Leonardo da Vinci Airport	Rome
Barcelona Airport	Barcelona
O'Hare International Airport	Chicago
Munich Airport	Munich
Phoenix Sky Harbor International Airport	Phoenix
John F. Kennedy International Airport	New York
Minneapolis-Saint Paul International Airport	Minneapolis
Atatürkü International Airport	Istanbul
Dubai International Airport	Dubai
Los Angeles International Airport	Los Angeles
London Gatwick Airport	London
Toronto Pearson International Airport	Toronto
Paris Charles de Gaulle Airport	Paris
Shanghai Pudong International Airport	Shanghai
Singapore Changi Airport	Singapore
Seoul Incheon International Airport	Seoul
London Heathrow Airport	London
Paris-Orly Airport	Paris
Frankfurt Airport	Frankfurt
Newark Liberty International Airport	Newark
Charlotte Douglas International Airport	Charlotte
Dublin Airport	Dublin
McCarran International Airport	Las Vegas
Dallas-Fort Worth International Airport	Dallas
Mexico City International Airport	Mexico City
Narita International Airport	Tokyo
Indira Gandhi International Airport	New Delhi
Tokyo International Airport	Tokyo
Madrid-Barajas Airport	Madrid
Chhatrapati Shivaji International Airport	Mumbai
Hartsfield-Jackson Atlanta International Airport	Atlanta
Washington Dulles International Airport	Washington D.C.
Suvarnabhumi Airport	Bangkok
Soekarno-Hatta International Airport	Jakarta
Sydney Airport	Sydney
Logan International Airport	Boston
Detroit Metropolitan Wayne County Airport	Detroit
Orlando International Airport	Orlando
Kuala Lumpur International Airport	Kuala Lumpur
George Bush Intercontinental Airport	Houston
Melbourne Airport	Melbourne
Guangzhou Baiyun International Airport	Guangzhou
Hong Kong International Airport	Hong Kong
Beijing Capital International Airport	Beijing
Miami International Airport	Miami
San Francisco International Airport	San Francisco
Seattle-Tacoma International Airport	Seattle
Philadelphia International Airport	Philadelphia
Amsterdam Airport Schiphol	Amsterdam
\.


--
-- Data for Name: airport_abrev; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.airport_abrev (name) FROM stdin;
PVG
LAX
CDG
CLT
JFK
NRT
DFW
MUC
SYD
BOM
BKK
KUL
MIA
HKG
AMS
BOS
BCN
IAD
SEA
DXB
MAD
IAH
CAN
FCO
MEL
SIN
YYZ
LGW
ORD
MEX
DTW
DUB
PHL
LHR
ORY
SFO
PHX
EWR
CGK
DEL
MSP
IST
DEN
FRA
ICN
PEK
MCO
ATL
HND
LAS
\.


--
-- Data for Name: airport_transl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.airport_transl (fullname, shortname) FROM stdin;
Hartsfield-Jackson Atlanta International Airport	ATL
O'Hare International Airport	ORD
London Heathrow Airport	LHR
Tokyo International Airport	HND
Paris Charles de Gaulle Airport	CDG
Los Angeles International Airport	LAX
Dallas-Fort Worth International Airport	DFW
Beijing Capital International Airport	PEK
Frankfurt Airport	FRA
Denver International Airport	DEN
Madrid-Barajas Airport	MAD
Hong Kong International Airport	HKG
John F. Kennedy International Airport	JFK
Amsterdam Airport Schiphol	AMS
McCarran International Airport	LAS
George Bush Intercontinental Airport	IAH
Phoenix Sky Harbor International Airport	PHX
Suvarnabhumi Airport	BKK
Singapore Changi Airport	SIN
Dubai International Airport	DXB
San Francisco International Airport	SFO
Orlando International Airport	MCO
Newark Liberty International Airport	EWR
Detroit Metropolitan Wayne County Airport	DTW
Leonardo da Vinci Airport	FCO
Charlotte Douglas International Airport	CLT
Munich Airport	MUC
London Gatwick Airport	LGW
Miami International Airport	MIA
Minneapolis-Saint Paul International Airport	MSP
Narita International Airport	NRT
Guangzhou Baiyun International Airport	CAN
Sydney Airport	SYD
Toronto Pearson International Airport	YYZ
Seattle-Tacoma International Airport	SEA
Soekarno-Hatta International Airport	CGK
Philadelphia International Airport	PHL
Barcelona Airport	BCN
Seoul Incheon International Airport	ICN
Shanghai Pudong International Airport	PVG
Kuala Lumpur International Airport	KUL
AtatÃ¼rk International Airport	IST
Mexico City International Airport	MEX
Paris-Orly Airport	ORY
Logan International Airport	BOS
Melbourne Airport	MEL
Chhatrapati Shivaji International Airport	BOM
Washington Dulles International Airport	IAD
Dublin Airport	DUB
Indira Gandhi International Airport	DEL
\.


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
-- Data for Name: animalowner1row; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.animalowner1row (owner_id, animalname, category) FROM stdin;
1	bill	chien
\.


--
-- Data for Name: artists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artists (id, name, language) FROM stdin;
1	Taylor Swift	English
2	Reputation Artist	English
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
-- Data for Name: bakery_salesitemoven_temperatureitem_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bakery_salesitemoven_temperatureitem_table (word, synonym) FROM stdin;
Croissants	Croissants
Baguettes	Baguettes
Macarons	Macarons
Pain au Chocolat	Pain au Chocolat
\.


--
-- Data for Name: chemical; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chemical (name, melting_point) FROM stdin;
Methane	-182.5
Water	0
Lead (IV) Bromide	380
Copper (II) Nitrate	565
Zince Sulfide	1180
Iron (II) Sulfide	1190
Ammonium Sulfide	-80
Copper (II) sulfate	1100
Silver Chromate	765
Magnesium Chromate	1000
Carbon monoxide	-205
Silver Hydroxide	220
Ammonium Bromide	-93
Iron (II) Acetate	260
Mercury (I) Acetate	200
Potassium Carbonate	890
Calcium Sulfate	1450
Iron (II) Sulfate	870
Potassium Iodide	681
Zinc Chloride	778
Barium Hydroxide	730
Calcium Carbonate	825
Iron (III) Phosphate	1250
Lead (II) Nitrate	243
Zinc Acetate	310
Mercury (II) Nitrate	470
Mercury (I) Chromate	380
Ammonium Acetate	118
Sodium Nitrate	308
Calcium Sulfide	2550
Lead (IV) Iodide	410
Lead (IV) Sulfate	800
Aluminum Hydroxide	1300
Mercury (I) Sulfide	600
Iron (III) Iodide	575
Potassium Nitrate	334
Hydrogen sulfide	-85.5
Mercury (II) Chromate	460
Zinc Bromide	762
Zinc Sulfate	1123
Oxygen	-218.4
Potassium Phosphate	600
Barium Sulfate	1370
Lead (IV) Sulfide	900
Copper (II) Chromate	770
Sodium Chromate	800
Copper (II) Chloride	417
Sodium Iodide	661
Barium Sulfide	1800
Lead (II) Hydroxide	280
Aluminum Sulfide	1550
Iron (II) Carbonate	850
Mercury (II) Iodide	315
Ammonium Phosphate	160
Copper (II) Carbonate	400
Lead (IV) Chromate	610
Lead (IV) Hydroxide	300
Iron (III) Nitrate	160
Aluminum Chromate	1000
Iron (III) Hydroxide	300
Barium Nitrate	590
Silver Sulfate	1000
Silver Sulfide	1650
Ammonium Carbonate	120
Lead (II) Iodide	405
Magnesium Acetate	115
Aluminum Sulfate	650
Lead (II) Chromate	870
Lead (II) Chloride	501
Sodium Phosphate	300
Iron (II) Phosphate	785
Calcium Acetate	330
Sulfur dioxide	-75.5
Magnesium Hydroxide	350
Copper (II) Sulfide	1100
Sodium Sulfide	890
Iron (II) Chromate	640
Copper (II) Phosphate	960
Mercury (I) Phosphate	480
Hydrogen fluoride	-83
Iron (II) Chloride	677
Calcium Bromide	772
Calcium Chloride	772
Silver Nitrate	212
Chlorine	-101
Mercury (I) Carbonate	320
Calcium Chromate	800
Nitrogen	-210
Ammonia	-77.7
Merucry (II) Chloride	270
Iron (II) Nitrate	118
Mercury (I) Iodide	320
Iron (II) Bromide	650
Copper (II) Sulfate	1100
Aluminum Nitrate	205
Sodium Sulfate	884
Aluminum Carbonate	2200
Aluminum Iodide	1200
Lead (II) oxide	880
Zinc Hydroxide	525
Potassium Sulfate	1069
Hydrogen iodide	-50.8
Carbon dioxide	-78.5
Sodium Carbonate	851
Lead (II) Sulfide	1100
Aluminum Phosphate	1280
Mercury (I) Nitrate	170
Calcium Hydroxide	580
Copper (II) Bromide	430
Barium Chromate	970
Ethyne (acetylene)	-80.8
Magnesium Phosphate	1250
Silver Carbonate	230
Ammonium Chloride	338
Aluminun oxide	2072
Merucry (I) Chloride	270
Lead (IV) Nitrate	225
Aluminum Chloride	193
Ammonium Nitrate	169
Sodium Bromide	755
Lead (II) Carbonate	840
Lead (IV) Phosphate	980
Copper (II) Acetate	370
Zinc Nitrate	250
Barium Phosphate	980
Potassium Chloride	770
Potassium Sulfide	1100
Potassium chloride	770
Iron (II) Iodide	500
Mercury (II) Bromide	285
Potassium Acetate	302
Lead (II) Acetate	290
Iron (III) Chloride	315
Iron (III) Chromate	615
Potassium Chromate	398
Hydrogen chloride	-114.2
Silver Acetate	330
Silver Phosphate	1700
Potassium Hydroxide	360
Sodium Acetate	325
Copper (II) Iodide	420
Merucry (I) Hydroxide	320
Magnesium Bromide	710
Sodium Chloride	801
Calcium Nitrate	561
Silver Bromide	432
Aluminum Acetate	130
Sodium chloride	801
Lead (II) Phosphate	825
Iodine chloride	27.2
Aluminum Bromide	97.5
Barium Carbonate	1360
Iron (III) Acetate	160
Mercury (II) Hydroxide	300
Calcium Iodide	772
Silver Chloride	455
Magnesium Sulfate	1124
Merucry (II) Sulfate	500
Barium Acetate	300
Barium Chloride	960
Magnesium Chloride	712
Zinc Chromate	930
Mercury (II) Phosphate	490
Iron (III) Bromide	200
Nitrogen (IV) oxide	21.1
Barium Bromide	690
Magnesium Sulfide	2000
Magnesium oxide	2852
Barium Iodide	900
Copper (II) Hydroxide	80
Ethene (ethylene)	-169
Ammonium Iodide	171
Merucry (II) Acetate	420
Zinc Phosphate	1000
Calcium hydroxide	580
Nitrogen (II) oxide	-90.8
Hydrogen	-259.1
Silver Iodide	652
Mercury (II) Carbonate	390
Mercury (I) Sulfate	500
Zinc Iodide	419
Iron (III) Sulfide	1100
Magnesium Nitrate	255
Iron (III) Sulfate	980
Lead (II) Bromide	420
Magnesium Carbonate	840
Potassium Bromide	730
Magnesium Iodide	630
Ammonium Chromate	170
Ammonium Sulfate	280
Mercury (II) Sulfide	589
Ethane	-88.6
Lead (II) Sulfate	818
Mercury (I) Bromide	200
Lead (IV) Acetate	300
Iron (III) Carbonate	1000
Iron (II) Hydroxide	580
Ammonium Hydroxide	-77.7
Sodium Hydroxide	318
Calcium Phosphate	1500
Zinc Carbonate	1900
\.


--
-- Data for Name: chemical_abrev; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chemical_abrev (name_abrev) FROM stdin;
CuS
FeCO3
Hg3PO4
Pb(C2H3O2)2
Al2S3
Pb(C2H3O2)4
FeI3
FeI2
FeSO4
KCl
CuBr2
CaI2
Fe(C2H3O2)2
ZnCrO4
Mg(OH)2
AlPO4
Fe2(SO4)3
Fe3(PO4)2
Pb3(PO4)2
Pb3(PO4)4
Fe(C2H3O2)3
Mg(NO3)2
KNO3
HgI2
ZnCO3
CaCl2
Ag2CrO4
AlBr3
CuSO4
KC2H3O2
HgBr2
MgI2
CO
Ca3(PO4)2
CH4
(NH4)3PO4
PbO
MgCrO4
AgOH
PbS
AgC2H3O2
K2CrO4
K2SO4
AlI3
FeBr2
FeBr3
Pb(CO3)2
Al2O3
NO2
Al(C2H3O2)3
ICl
CuCO3
PbSO4
Pb(SO4)2
K2CO3
Al(OH)3
HgCrO4
Na2CO3
MgCl2
ZnSO4
H2O
Zn(C2H3O2)2
H2S
Fe(NO3)3
Fe(NO3)2
Cu(C2H3O2)2
Zn(NO3)2
Na2SO4
PbI4
Fe2S3
PbI2
AgI
CuCrO4
Cl2
NaOH
Ba(NO3)2
ZnBr2
Fe(OH)3
BaBr2
Fe(OH)2
HCl
Ba(OH)2
FeCrO4
NaI
NH4C2H3O2
FePO4
PbBr2
Ag3PO4
PbBr4
Zn(OH)2
H2
Cu(NO3)2
Al2(CO3)3
HF
HI
Ca(C2H3O2)2
HgI
Ca(OH)2
(NH4)2CrO4
(NH4)2CO3
CuCl2
Mg3(PO4)2
HgS
HgOH
(NH4)2SO4
MgCO3
Zn2(PO4)2
Hg2SO4
Ba3(PO4)2
AgBr
Al2(SO4)3
MgSO4
HgNO3
Ag2S
CuI2
CO2
BaCO3
Hg3(PO4)2
AgNO3
AgCl
Na2S
FeS
BaSO4
SO2
AlCl3
CaBr2
(NH4)2S
Hg(NO3)2
KI
NaC2H3O2
Na2CrO4
PbCO3
C2H6
Hg2CrO4
C2H4
BaCrO4
KOH
C2H2
HgCl2
ZnI2
Ba(C2H3O2)2
ZnS
NH4OH
FeCl3
Ag2SO4
FeCl2
Al2(CrO4)3
Cu3(PO4)2
CaS
Pb(NO3)4
Pb(NO3)2
Fe2(CrO4)3
Pb(OH)4
Pb(OH)2
N2
MgBr2
NaBr
NaNO3
PbCrO4
NH4Cl
NH4NO3
HgC2H3O2
Ag2CO3
BaI2
NH3
NaCl
NO
O2
BaCl2
NH4Br
CaSO4
Hg(C2H3O2)2
HgCl
Ca(NO3)2
ZnCl2
MgO
CaCO3
Hg2CO3
BaS
MgS
CaCrO4
Cu(OH)2
Na3PO4
Al(NO3)3
Hg2S
PbCl2
Fe2(CO3)3
Mg(C2H3O2)2
NH4I
HgBr
K2S
HgCO3
K3PO4
PbS2
Hg(OH)2
KBr
HgSO4
\.


--
-- Data for Name: chemical_translations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chemical_translations (full_name, short_name) FROM stdin;
Ammonia	NH3
Carbon dioxide	CO2
Carbon monoxide	CO
Chlorine	Cl2
Hydrogen chloride	HCl
Hydrogen	H2
Hydrogen sulfide	H2S
Methane	CH4
Nitrogen	N2
Nitrogen (II) oxide	NO
Oxygen	O2
Sulfur dioxide	SO2
Aluminum oxide	Al2O3
Barium Sulfate	BaSO4
Calcium hydroxide	Ca(OH)2
Copper (II) sulfate	CuSO4
Ethane	C2H6
Ethene (ethylene)	C2H4
Ethyne (acetylene)	C2H2
Hydrogen fluoride	HF
Hydrogen iodide	HI
Iodine chloride	ICl
Lead (II) oxide	PbO
Magnesium oxide	MgO
Nitrogen (II) oxide	NO
Nitrogen (IV) oxide	NO2
Potassium chloride	KCl
Sodium chloride	NaCl
Sulfur dioxide	SO2
Water	H2O
Aluminum Bromide	AlBr3
Aluminum Carbonate	Al2(CO3)3
Aluminum Chloride	AlCl3
Aluminum Chromate	Al2(CrO4)3
Aluminum Hydroxide	Al(OH)3
Aluminum Iodide	AlI3
Aluminum Nitrate	Al(NO3)3
Aluminum Phosphate	AlPO4
Aluminum Sulfate	Al2(SO4)3
Aluminum Sulfide	Al2S3
Ammonium Acetate	NH4C2H3O2
Ammonium Bromide	NH4Br
Ammonium Carbonate	(NH4)2CO3
Ammonium Chloride	NH4Cl
Ammonium Chromate	(NH4)2CrO4
Ammonium Hydroxide	NH4OH
Ammonium Iodide	NH4I
Ammonium Nitrate	NH4NO3
Ammonium Phosphate	(NH4)3PO4
Ammonium Sulfate	(NH4)2SO4
Ammonium Sulfide	(NH4)2S
Barium Acetate	Ba(C2H3O2)2
Barium Bromide	BaBr2
Barium Carbonate	BaCO3
Barium Chloride	BaCl2
Barium Chromate	BaCrO4
Barium Hydroxide	Ba(OH)2
Barium Iodide	BaI2
Barium Nitrate	Ba(NO3)2
Barium Phosphate	Ba3(PO4)2
Barium Sulfate	BaSO4
Barium Sulfide	BaS
Calcium Acetate	Ca(C2H3O2)2
Calcium Bromide	CaBr2
Calcium Carbonate	CaCO3
Calcium Chloride	CaCl2
Calcium Chromate	CaCrO4
Calcium Hydroxide	Ca(OH)2
Calcium Iodide	CaI2
Calcium Nitrate	Ca(NO3)2
Calcium Phosphate	Ca3(PO4)2
Calcium Sulfate	CaSO4
Calcium Sulfide	CaS
Copper (II) Acetate	Cu(C2H3O2)2
Copper (II) Bromide	CuBr2
Copper (II) Carbonate	CuCO3
Copper (II) Chloride	CuCl2
Copper (II) Chromate	CuCrO4
Copper (II) Hydroxide	Cu(OH)2
Copper (II) Iodide	CuI2
Copper (II) Nitrate	Cu(NO3)2
Copper (II) Phosphate	Cu3(PO4)2
Copper (II) Sulfate	CuSO4
Copper (II) Sulfide	CuS
Iron (II) Acetate	Fe(C2H3O2)2
Iron (II) Bromide	FeBr2
Iron (II) Carbonate	FeCO3
Iron (II) Chloride	FeCl2
Iron (II) Chromate	FeCrO4
Iron (II) Hydroxide	Fe(OH)2
Iron (II) Iodide	FeI2
Iron (II) Nitrate	Fe(NO3)2
Iron (II) Phosphate	Fe3(PO4)2
Iron (II) Sulfate	FeSO4
Iron (II) Sulfide	FeS
Iron (III) Acetate	Fe(C2H3O2)3
Iron (III) Bromide	FeBr3
Iron (III) Carbonate	Fe2(CO3)3
Iron (III) Chloride	FeCl3
Iron (III) Chromate	Fe2(CrO4)3
Iron (III) Hydroxide	Fe(OH)3
Iron (III) Iodide	FeI3
Iron (III) Nitrate	Fe(NO3)3
Iron (III) Phosphate	FePO4
Iron (III) Sulfate	Fe2(SO4)3
Iron (III) Sulfide	Fe2S3
Magnesium Acetate	Mg(C2H3O2)2
Magnesium Bromide	MgBr2
Magnesium Carbonate	MgCO3
Magnesium Chloride	MgCl2
Magnesium Chromate	MgCrO4
Magnesium Hydroxide	Mg(OH)2
Magnesium Iodide	MgI2
Magnesium Nitrate	Mg(NO3)2
Magnesium Phosphate	Mg3(PO4)2
Magnesium Sulfate	MgSO4
Magnesium Sulfide	MgS
Mercury (I) Acetate	HgC2H3O2
Mercury (I) Bromide	Hg2Br2
Mercury (I) Carbonate	Hg2CO3
Mercury (I) Chloride	Hg2Cl2
Mercury (I) Chromate	Hg2CrO4
Mercury (I) Hydroxide	Hg2(OH)2
Mercury (I) Iodide	Hg2I2
Mercury (I) Nitrate	Hg2(NO3)2
Mercury (I) Phosphate	Hg3(PO4)2
Mercury (I) Sulfate	Hg2SO4
Mercury (I) Sulfide	Hg2S
Mercury (II) Acetate	Hg(C2H3O2)2
Mercury (II) Bromide	HgBr2
Mercury (II) Carbonate	HgCO3
Mercury (II) Chloride	HgCl2
Mercury (II) Chromate	HgCrO4
Mercury (II) Hydroxide	Hg(OH)2
Mercury (II) Iodide	HgI2
Mercury (II) Nitrate	Hg(NO3)2
Mercury (II) Phosphate	Hg3(PO4)2
Mercury (II) Sulfate	HgSO4
Mercury (II) Sulfide	HgS
Potassium Acetate	KC2H3O2
Potassium Bromide	KBr
Potassium Carbonate	K2CO3
Potassium Chloride	KCl
Potassium Chromate	K2CrO4
Potassium Hydroxide	KOH
Potassium Iodide	KI
Potassium Nitrate	KNO3
Potassium Phosphate	K3PO4
Potassium Sulfate	K2SO4
Potassium Sulfide	K2S
Silver Acetate	AgC2H3O2
Silver Bromide	AgBr
Silver Carbonate	Ag2CO3
Silver Chloride	AgCl
Silver Chromate	Ag2CrO4
Silver Hydroxide	AgOH
Silver Iodide	AgI
Silver Nitrate	AgNO3
Silver Phosphate	Ag3PO4
Silver Sulfate	Ag2SO4
Silver Sulfide	Ag2S
Sodium Acetate	NaC2H3O2
Sodium Bromide	NaBr
Sodium Carbonate	Na2CO3
Sodium Chloride	NaCl
Sodium Chromate	Na2CrO4
Sodium Hydroxide	NaOH
Sodium Iodide	NaI
Sodium Nitrate	NaNO3
Sodium Phosphate	Na3PO4
Sodium Sulfate	Na2SO4
Sodium Sulfide	Na2S
Zinc Acetate	Zn(C2H3O2)2
Zinc Bromide	ZnBr2
Zinc Carbonate	ZnCO3
Zinc Chloride	ZnCl2
Zinc Chromate	ZnCrO4
Zinc Hydroxide	Zn(OH)2
Zinc Iodide	ZnI2
Zinc Nitrate	Zn(NO3)2
Zinc Phosphate	Zn3(PO4)2
Zinc Sulfate	ZnSO4
Zinc Sulfide	ZnS
Lead (II) Acetate	Pb(C2H3O2)2
Lead (II) Bromide	PbBr2
Lead (II) Carbonate	PbCO3
Lead (II) Chloride	PbCl2
Lead (II) Chromate	PbCrO4
Lead (II) Hydroxide	Pb(OH)2
Lead (II) Iodide	PbI2
Lead (II) Nitrate	Pb(NO3)2
Lead (II) Phosphate	Pb3(PO4)2
Lead (II) Sulfate	PbSO4
Lead (II) Sulfide	PbS
Lead (IV) Acetate	Pb(C2H3O2)4
Lead (IV) Bromide	PbBr4
Lead (IV) Chromate	PbCrO4
Lead (IV) Hydroxide	Pb(OH)4
Lead (IV) Iodide	PbI4
Lead (IV) Nitrate	Pb(NO3)4
Lead (IV) Phosphate	Pb3(PO4)4
Lead (IV) Sulfate	Pb(SO4)2
Lead (IV) Sulfide	PbS2
Aluminum Acetate	Al(C2H3O2)3
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
-- Data for Name: children_tableidfathersid_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.children_tableidfathersid_table (word, synonym) FROM stdin;
0	zero
1	one
2	two
\.


--
-- Data for Name: doctors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctors (id, name, patients_pd) FROM stdin;
3	Hans	fourty
4	Lukas	44
1	Peter	ten
5	Dr. Smith	150
2	Giovanni	11
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (content, embedding) FROM stdin;
1	[-0.023078628,0.06686101,-0.08202705,-0.024811246,0.023489092,-0.013869977,0.04166449,0.052001063,-0.05799491,0.038271844,0.019840544,0.008990711,0.049446564,0.012066826,-0.005654009,-0.0989573,0.033384673,-0.004052895,-0.1000304,0.021898547,-0.0018112295,-0.035587747,0.057477254,-0.020952499,-0.023169486,-0.031574596,0.013504972,-0.029827608,-0.038192928,-0.026186192,0.09176392,0.06755935,0.023920683,-0.023388682,0.06389691,0.06521887,0.016392536,0.05379386,0.023575611,-0.018889189,-0.059247848,0.0011639323,0.0041168435,0.043775626,-0.040863376,-0.007877535,0.0056439205,0.0332707,-0.03281183,0.03732632,0.042258617,0.05833592,-0.021431504,0.015222269,-0.05823442,-0.03962728,-0.0028944942,-0.019235115,0.013108683,-0.04195565,-0.002363694,-0.027593693,-0.008516751,-0.011897348,-0.039843198,-0.017581383,-0.03070107,0.046166968,-0.11986905,0.051790953,0.029902525,0.042342223,-0.026438896,0.006177764,0.0045847353,-0.04052613,0.03382912,0.022459375,-0.031225061,0.027317157,-0.036349654,0.032253515,0.027411671,0.009583643,-0.020073606,-0.0008401292,0.0056680986,-0.020944204,-0.049348153,-0.033235263,0.040292222,0.029044539,0.023561388,0.043365605,-0.0029468068,-0.09774329,-0.06425326,-0.0793769,0.021547992,0.09703167,0.046798736,-0.0022515398,0.000679287,-0.03557579,0.047252163,0.06313589,-0.053032752,-0.022348953,-0.03977059,0.0010494872,-0.0125780795,-0.059365757,0.01917739,-0.05646845,0.030221395,-0.06567988,0.0021012567,-0.015987253,0.031443726,-0.0041242084,0.004588368,0.0512053,-0.0003089184,-0.018815508,0.051937174,0.016758054,0.0033875639,-0.02139352,-0.014426234,0.01960802,0.13197586,-0.06149075,0.011124072,0.013844287,0.01795478,-0.048103753,0.0824293,0.02886111,0.018637577,0.038467243,0.034426153,-0.020640673,-0.08793113,0.024816463,0.011351059,-0.05116774,0.0750904,0.045637894,-0.05647248,-0.03304205,0.005103994,-0.015876004,0.010862813,0.011826139,-0.009656885,-0.0033435395,0.073418744,-0.049747422,0.0651019,-0.015000219,-0.0027792517,-0.054636702,0.022813361,0.009038886,-0.031868543,0.00687038,0.003391259,-0.03894381,0.039361443,0.0076223747,-0.015699191,-0.002724506,-0.013668715,-0.031393077,-0.031165129,0.009178812,-0.021319307,-0.017169189,0.0006524169,0.06515655,0.0692456,0.049343918,0.023250114,-0.076465525,0.019896727,0.034516294,0.029391393,0.033965748,0.039176997,0.07031003,-0.049936663,-0.003106769,0.016158352,0.064558946,0.012408864,-0.006998691,0.038216434,0.025920328,-0.070730895,-0.06238122,0.046021234,-0.057307154,0.0037244589,-0.032823287,0.012693649,-0.009676317,-0.043894056,-0.050593395,0.06971981,0.0010599843,0.029752273,-0.030041134,0.023545684,-0.0028867389,0.0254688,-0.01059958,0.062062,-0.006774234,0.02858246,0.055624418,0.002089135,-0.012389227,-0.0019134792,0.021989377,0.022126881,0.043805413,-0.030340001,-0.051583376,0.027908938,-0.027806569,-0.015406742,0.0094210375,0.045025133,0.00386626,0.034962088,0.030471077,-0.007718845,-0.04917825,-0.064866215,-0.010460424,-0.020652749,0.0498811,0.0046671513,-0.0005072688,0.035373755,0.059888925,0.011859163,0.019681383,-0.04451413,-0.078343734,-0.027847655,-0.0304546,-0.045722123,-0.08446138,0.004452652,-0.019164247,0.022859614,0.013209188,0.011090886,-0.00065925566,0.027836198,-0.062736444,0.013039273,-0.037735928,-0.026503801,-0.032629818,-0.0068904697,-0.035767347,0.0449107,-0.09472595,0.026106635,-0.0049785185,-0.008901859,-0.0146417795,0.05176996,0.012261913,0.0030696315,-0.010750445,0.0019454684,-0.007961587,-0.030563109,0.0020282236,0.011584477,-0.0005889951,-0.020536724,-0.081059836,-0.0004956827,-0.0009567815,-0.024062486,0.0034919025,0.027946947,0.08039943,0.015904969,-0.038216483,0.072976395,0.02649001,0.04880313,-0.019308256,0.009401889,-0.023193818,0.09045448,0.04811627,0.02936209,0.0412743,0.02065284,0.03693938,0.05976862,-0.068053715,0.039346565,0.009944521,0.016502349,0.01939826,-8.096459e-05,-0.03917304,-0.047253348,0.011074064,-0.15337336,0.0091242185,-0.032583755,-0.006748249,-0.039093673,0.032536123,0.004634046,-0.023687327,0.038575538,-0.008402603,-0.026245035,0.012150974,0.03024642,-0.022756927,0.01824844,0.06005483,-0.022419494,-0.06665428,0.0466223,-0.0329539,-0.004450761,0.021845896,0.03615521,-0.015599803,-0.0049632327,0.019952247,0.034214754,0.05227675,0.0012621632,-0.062105816,-0.011737458,-0.01995856,0.035947464,0.007672632,-0.02013422,0.023983806,-0.0053800694,-0.011874669,-0.029093962,0.022428527,0.07181907,0.015400267,0.029140074,-0.020516772,0.02744558,-0.032994688,0.0112899225,-0.019134142,-0.027381836,-0.052451428,-0.016278252,0.0074891895,-0.020329563,0.00034529838,0.0354871,-0.008434288,-0.0045887907,0.006649814,-0.02287112,-0.017770763,-0.0031518654,0.01884344,0.040297154,-0.021641891,-0.046962634,-0.0069479733,-0.0022811107,-0.0043885084,-0.06983137,0.08039511,-0.030694481,-0.012186783,0.03261753,-0.018219808,-0.008994442,0.0037384867,0.053675532,0.0008233336,0.024887428,0.025578992,-0.00383902,0.045165066,0.018595126,0.04776987,-0.029972373,-0.028913775,0.07746541,0.009723171,-0.0047919657,0.007057198,0.050845254,0.011970747,0.008576805,0.032379143,-0.006558096,0.031718716,-0.0550067,0.008399927,-0.045399025,0.005393787,-0.015569452,0.03031189,-0.0032448021,0.024637988,-0.03966872,-0.0032118158,-0.014140487,0.016895458,0.03623944,-0.09303055,-0.015862472,-0.0019617465,0.033448193,0.007572629,0.030273939,-0.01858747,0.02718954,0.03204336,0.04557314,-0.020451143,-0.011892895,-0.035127025,-0.053367347,-0.028530536,0.011263202,-0.03699803,-0.038405206,0.07311872,-0.060781796,0.010310438,0.010074503,0.010191741,0.0045905258,0.016386528,-0.032964688,-0.0043836087,-0.0712652,-0.0066783745,-0.025015587,0.0038010357,-0.001787939,-0.009757194,-0.02425428,0.06759615,-0.067021705,-0.017608492,0.01487648,-0.0011820338,0.0511966,-0.04215944,-0.022091502,0.080298714,-0.00528814,0.023104645,0.06600405,0.013306837,0.005686357,0.01825551,0.0020416526,0.028159289,0.045575228,0.0037566137,-0.009758748,-0.008749228,0.009420847,0.023672514,-0.018352482,0.03452163,0.055262085,-0.057182904,-0.044735238,-0.0049715172,0.067163266,0.044289313,0.022090614,0.017247945,-0.017343942,-0.032221075,0.06519922,0.03649633,-0.019540418,0.0027035659,0.0077764774,0.060383298,0.052105792,-0.019634932,-0.01716508,-0.056719452,-0.016660485,0.006643481,-0.052239925,-0.04992086,0.038810275,-0.030854244,0.0036253657,-0.0062771603,0.0044847955,-0.017000807,-0.01984801,0.016618714,-0.060272045,0.042806283,0.00037469793,0.02406587,-0.034093346,0.00084808364,-0.0047832727,0.0043318556,-0.010421867,0.00823273,0.035375603,0.0103364205,-0.0073293974,-0.038319506,-0.06981339,0.05538773,0.02532067,0.08214748,-0.0014915207,0.026274413,-0.00544096,0.010365725,0.040404126,-0.03588421,-0.022953628,-0.009806936,-0.016176153,-0.020626787,0.027409464,0.013213412,-0.032494403,0.035219803,-0.017680576,0.066433795,0.011653323,-0.030037802,0.004873084,0.020875948,-0.014688591,-0.0006391462,-0.0115992995,-0.016998954,-0.050704725,0.026768167,0.0107150385,0.0009823188,-0.021284502,-0.036542483,-0.0008375694,-0.042955678,0.014734876,0.04567431,0.019881811,-0.022654882,-0.008859749,0.010608323,0.0071325963,-0.030293854,0.027545393,0.012612573,-0.032251537,-0.019313585,0.09015297,-0.01878142,0.051775828,0.025249906,0.051601615,-0.012916746,0.0021712543,0.01259899,0.047842145,0.010166591,0.0137349395,-0.006654854,-0.026287217,0.01617039,0.00080917956,-0.0368232,-0.02477761,-0.030850364,-0.04242699,-0.052944686,0.026275314,0.004691004,0.03327745,0.0033185296,0.02056269,0.043909363,-0.056901515,-0.10815165,-0.04016447,-0.020257005,-0.017060772,0.024802342,0.017262483,0.031312253,-0.06900682,0.048047066,-0.0072978656,0.014967139,0.016812446,-0.0038995545,0.016779495,0.0136752,-0.0062548514,-0.016026802,-0.020685766,-0.07302709,-0.008334243,-0.014883734,0.004034052,0.029078683,0.008439845,0.049973283,-0.0021206462,0.023222372,0.011601449,-0.014100699,-0.008936672,-0.008814172,0.018802552,-0.043799166,0.019530248,-0.026023103,0.010847241,0.032431133,0.07239589,-0.0017670355,-0.047175504,0.01553022,-0.020885542,-0.023285318,0.03252582,-0.003121177,0.0017794548,-0.0025170618,0.04002818,-0.027103378,-0.037890412,-0.011031781,-0.00093241996,-0.016423615,0.017117165,-0.042702153,-0.04284399,-0.03820114,0.044112653,0.0019476572,-0.03752886,-0.02899239,0.018684763,0.0041408334,-0.021465326,-0.029221244,0.06295235,-0.014287051,0.02801519,0.05858948,-0.041690208,0.0016626864,-0.004175269,-0.0034699761,0.0068775057,0.03957957,0.009361486,-0.0012039273,-0.020807292,-0.031023882,0.058027234,0.022180304,0.053372953,-0.043599732,-0.0005617218,-0.021977864,-0.01525407,-0.00859324,0.027726216,0.043350007,-0.02786882,0.016394382,-0.040913437,0.010719707,-0.028180087,-0.044083595,-0.016669722,0.0037536207,-0.08150312,-0.0044549955,0.028227152,0.0011618658,8.564049e-05,0.028822683,-0.06218146,-0.007807057,-0.0319859,0.04524244,0.009244133,0.02303477,0.030589443,-0.03710201,0.0024772403,0.022655101,0.0109664295,0.014860989,-0.031163367,-0.013450148,-0.0020887617,0.039093103,0.014932077,-0.031112121,-0.046702582,0.052592054,-0.080872506,0.048346408,0.037361607,-0.010849247,-0.039221287,0.023192812,0.01288508,-0.036173373,-0.031036038,0.040181395,-0.03678143,-0.00794914,0.04828058,-0.012329059,-0.030162774,0.008072341,0.023472063,0.0152858365,0.011385837,-0.022025494,-0.053673267,-0.018317485,-0.07246059,0.043895498,0.046115696,-8.614812e-06,0.03532197,-0.02350265,-0.004918873,-0.02146942,-0.00915546,0.0380372,-0.049516823,0.0124503905,-0.02514368,-0.031301983,-0.055347987,-0.006439323,0.04794192,-0.0064676004]
two	[-0.0012887231,0.07933112,-0.07852221,0.0054895882,0.044039525,-0.011484093,0.06971188,0.05898619,-0.06855616,0.041537434,0.01864856,0.020436808,0.04906484,0.028082239,-0.0076808506,-0.10792961,0.032520592,0.0125897005,-0.07748631,0.025248464,-0.017455176,-0.04023595,0.05595495,-0.0037940838,-0.027294714,-0.035974957,0.005708057,-0.022843529,-0.03804136,-0.039224986,0.08786571,0.07811786,0.034088053,-0.025715925,0.070020005,0.054815177,0.026381686,0.059106134,0.03313486,-0.008005335,-0.0752178,0.00529673,0.019755712,0.04683881,-0.049036648,0.00828964,0.0038907533,0.045452766,-0.022327052,0.034632258,0.03740486,0.06689293,-0.015824946,0.021519981,-0.065237805,-0.035625063,0.005308659,-0.023050388,0.008592024,-0.04515648,-0.016189706,-0.0055154553,0.0053887013,0.011702284,-0.032100193,-0.030644188,-0.010212349,0.045457847,-0.119843,0.07156033,0.05017392,0.022828553,-0.033925083,-0.004803059,0.009251431,-0.03442219,0.025615945,0.019872777,-0.015203233,0.033715025,-0.009647379,0.022855068,0.039028767,-0.0027639677,-0.024819732,-0.013977442,0.015832582,-0.021975063,-0.032815482,-0.023541884,0.043030508,0.019735232,0.013562455,0.052829944,-0.025680661,-0.11032658,-0.07583766,-0.06376574,0.037445925,0.09279569,0.031560577,0.004408549,0.0014829923,-0.030811828,0.050207946,0.05674305,-0.060415998,-0.015477399,-0.056838997,-0.004771551,0.008522363,-0.07365162,0.018943697,-0.036740128,0.016472638,-0.06640002,-0.0045041526,-0.028954852,0.028150892,-0.0041450276,-0.004557503,0.033285946,-0.0045512435,-0.0069160373,0.056144867,0.025487877,-0.0065492433,-0.04189788,-0.011244402,0.0012510713,0.110106066,-0.07274843,0.01067064,0.030783994,0.017705165,-0.04652533,0.07035263,0.019561244,0.015718997,0.05517872,0.028197957,-0.008527138,-0.08014072,0.012291382,-0.0026316645,-0.043266147,0.05844991,0.035729874,-0.06965563,-0.003871586,-0.008320478,-0.018437842,0.010839718,0.019039989,-0.0022287602,-0.019896425,0.064006165,-0.07119361,0.07174367,-0.0086922925,0.0031305773,-0.047282025,0.024958624,0.040283676,-0.013390874,-0.0060261996,0.0055751307,-0.028220395,0.030744487,0.018137844,-0.015986,0.00517236,-0.020121718,-0.02403559,-0.03731609,-0.010577274,-0.013840473,-0.006653812,0.015058645,0.06436913,0.06516061,0.039241493,0.020963129,-0.061719507,0.01813996,0.029311303,0.038679942,0.039209455,0.045192696,0.06199893,-0.053488027,0.007850975,0.014833383,0.07220947,0.020883579,-0.021957722,0.05290091,0.04009468,-0.066592984,-0.06743441,0.05328648,-0.06620697,0.0025189517,-0.052077945,0.002303513,-0.00019521547,-0.049924612,-0.044679616,0.05231658,0.0018915001,0.054579183,-0.017014332,0.0077294502,0.021878783,0.018172,-0.021864342,0.06577755,0.0084582195,0.01878968,0.07297272,0.00053157023,-0.010700179,0.0052217124,0.022477638,0.018711742,0.035951797,-0.010806909,-0.06686229,0.010025534,-0.027956793,-0.024098344,-0.006643495,0.03572732,-0.00437749,0.012467846,0.029091742,-0.027759973,-0.0674338,-0.07413493,-0.005412909,-0.01974239,0.036217634,-0.0017339237,0.004021286,0.03633317,0.068738446,0.009082683,0.012225073,-0.042989556,-0.054701623,-0.024843417,-0.02623419,-0.052036107,-0.085476734,0.0010168924,-0.02251064,-0.003991513,9.62455e-06,0.0012887621,0.011862736,0.009623082,-0.06884613,0.01662087,-0.03755602,-0.021941615,-0.048894454,-0.0030925383,-0.053437263,0.07134754,-0.095492914,0.03736715,-0.0072014173,0.0005138401,-0.0017897373,0.052136723,0.021572156,0.009740142,-0.015332728,0.014247304,-0.010099075,-0.047552284,0.0297827,0.01896929,-0.00060368737,-0.014511462,-0.06992496,-0.00773357,-0.008686172,-0.035277337,-0.0063391533,0.037848968,0.09353447,0.021245591,-0.012901446,0.07576097,0.01232069,0.047118884,0.00499204,0.0062280134,-0.027337518,0.09013415,0.046159066,0.03821825,0.037800387,0.024556575,0.030395364,0.053339686,-0.0654121,0.03528719,0.024707617,-0.003325422,0.032343537,-0.007381045,-0.045037188,-0.052565012,0.010440444,-0.1398182,0.016834985,-0.023728173,-0.0037762914,-0.023374809,0.02971445,0.0012764578,-0.020031767,0.043267265,0.024826795,-0.031844955,-0.019577777,0.044593643,-0.018122945,-0.004738579,0.050207976,-0.016484527,-0.0850921,0.04009246,-0.016568689,0.00808648,0.031447522,0.040877406,-0.008207304,-0.006302267,0.028622791,0.031195527,0.044249833,-0.0065352856,-0.06152288,-0.0129703665,-0.022725748,0.03667629,0.0021440613,-0.039478663,0.01647744,-0.011610401,-0.010082947,-0.01843036,0.034307588,0.06763389,0.013679196,-0.0022244893,-0.01005675,0.025922254,-0.026205717,0.0011014107,-0.0008777787,-0.021628639,-0.0565906,0.0034927216,0.00826363,-0.026741888,-0.0043306523,0.030192059,0.006619081,-0.009374287,0.017965222,-0.018986722,-0.021415565,-0.041095868,0.0060469713,0.032439254,-0.023802422,-0.04034621,-0.006122616,-0.0044847443,-0.004422103,-0.07534296,0.07436522,-0.03156115,-0.01000175,0.028473686,-0.004990529,-0.011805984,0.002849522,0.053689297,0.0085904915,0.028546762,0.035261553,0.016195653,0.05285258,0.023158386,0.053488996,-0.011026168,-0.021246115,0.043243032,-0.012426461,0.009421312,0.011667088,0.047731016,-0.001750344,0.010498116,0.030121733,-0.005282872,0.01135605,-0.056376886,-0.025779678,-0.032028615,0.0007790951,-0.008830876,0.03132405,-0.011947225,0.009368001,-0.019506963,-0.008484266,0.0152400015,0.022253748,0.027830234,-0.09434984,-0.026994513,-0.0054971282,0.010385089,0.012431798,0.015484141,-0.021873375,0.0028783574,0.029566092,0.06704242,-0.012619707,0.015161921,-0.040196136,-0.05079102,-0.02936384,0.018517107,-0.035619132,-0.029664736,0.07372857,-0.045985576,0.012016862,0.0037563192,-0.0013964607,0.013175311,0.017457925,-0.01925059,-0.0033003574,-0.074148856,-0.0035060642,0.009759699,-0.0046719606,-0.0035771441,-0.014319297,-0.02112904,0.07016184,-0.059356607,-0.025095453,0.0061894846,-0.00076206034,0.0407433,-0.028752552,-0.00539421,0.07293563,-0.01170111,0.022435285,0.032498464,0.006100002,-0.022317823,0.020245064,-0.010778257,0.006460019,0.039530195,-0.0020232538,0.00023239611,0.0022546262,0.008061502,0.018978696,-0.014160041,0.044079527,0.04514912,-0.042304967,-0.01314326,-0.0041795266,0.061446216,0.043176908,0.02418098,0.022115603,-0.009969135,-0.03991961,0.053809986,0.031275492,-0.016412819,0.021107832,0.0082868375,0.060607493,0.06602226,-0.019509839,-0.036074,-0.05047987,-0.032441255,0.024170225,-0.038644493,-0.049184285,0.05715221,-0.04073084,0.0016494193,-0.0093280375,-0.004954047,-0.030092174,-0.022508489,0.020984326,-0.047362804,0.05546891,-0.00083763065,0.024517437,-0.037549812,0.0036243927,0.01963457,0.010958951,-0.013063661,0.0040283888,0.03488223,0.0013740681,-0.018004393,-0.050608188,-0.049915683,0.039396577,0.019784015,0.09486924,0.0030022445,0.024832467,0.0025228993,0.0106431255,0.029248286,-0.028570408,-0.026466627,-0.013114141,0.0020967482,-0.02790335,0.044332657,0.0049545676,-0.032539103,0.035279367,-0.028734557,0.07200358,0.0073308316,-0.023913048,0.0026148234,0.013674996,-0.012509793,-0.00216991,0.012545921,-0.01109906,-0.03986067,0.027276522,-0.0047025494,0.012840585,-0.026948297,-0.024693055,-0.008740466,-0.047261156,0.018960457,0.036472663,0.01604993,-0.032841742,-0.005289227,-0.0036313492,0.018720165,-0.024282143,0.011327696,0.022326596,-0.046288576,-0.007493387,0.0949252,-0.008359884,0.03522227,0.020557122,0.041640148,-0.0048558265,0.007797197,0.014046678,0.03600844,-0.0055289413,0.005773865,-0.021894203,-0.02984802,0.004974971,0.0065252883,-0.019484593,-0.033842802,-0.027915882,-0.024760379,-0.061791882,0.035682354,0.0017207297,0.03805548,-0.0053108684,0.03717946,0.048668824,-0.062193938,-0.094975084,-0.05627834,0.0013768601,-0.011182777,0.048171356,0.0029642154,0.024022244,-0.05573054,0.053203057,0.00022314333,0.0046971454,0.03228711,-0.012866354,0.012751624,0.019972922,-0.016668087,0.000941167,-0.025426902,-0.06673373,-0.01768314,-0.0040085423,0.02464574,0.02083144,0.008031789,0.03301128,-0.00042806205,0.04415344,-0.0046730987,0.00908765,-0.008786807,0.016852748,0.006282106,-0.041210994,0.01015192,-0.003691282,0.03081832,0.029555485,0.06931696,0.0185865,-0.044431474,0.0131053915,-0.02746022,-0.027879465,0.029977145,-0.019559024,-0.012867955,0.014650381,0.04674255,-0.019301694,-0.029345134,-0.013690641,-0.033301454,-0.03487141,0.017474532,-0.045443293,-0.045451432,-0.029396638,0.03442852,0.01872539,-0.01895297,-0.012546338,0.028584864,0.003819007,-0.011271742,-0.0068300553,0.06351471,-0.022683933,0.026905797,0.064761505,-0.04269866,0.015245995,-0.00074623455,-0.0057216473,-0.0021056382,0.019704783,0.004788723,-0.01722088,-0.007426387,-0.020530546,0.0636021,0.03150397,0.06490345,-0.045998253,0.003301668,-0.02239159,-0.023164978,0.0028227905,0.023568457,0.04282869,-0.038924478,0.032859024,-0.054892763,0.02545287,-0.025519561,-0.0439967,-0.013862526,0.017130006,-0.06991518,-0.0013918084,0.036121625,0.0132325515,-0.017417459,0.041119874,-0.0625819,-0.0030612154,-0.030306341,0.04444192,-0.0011992474,0.030119712,0.02452436,-0.03690553,-0.00047904035,0.00885927,0.0070349947,0.020254835,-0.025435252,-0.016456222,0.0021357154,0.045578483,0.027539553,-0.031745847,-0.047233365,0.05467224,-0.067560546,0.055154234,0.055090122,0.00047989996,-0.038497776,0.0060309027,0.03047733,-0.019075816,-0.021656489,0.026362851,-0.02399773,-0.00803919,0.044230424,0.0041880426,-0.04756865,0.003881328,0.017180717,0.029920187,0.003080367,-0.029498758,-0.039577346,0.0009288969,-0.07901472,0.02741769,0.025586406,0.009510512,0.036417287,-0.027535161,-0.010344305,-0.020298548,-0.013841312,0.03421051,-0.059939038,0.009351052,-0.03624271,-0.036468025,-0.043054327,0.013058195,0.04486638,-1.6707074e-05]
three	[0.01032337,0.0827647,-0.0664412,0.0019028403,0.040198628,-0.024088878,0.06371823,0.059975095,-0.048588436,0.055743307,0.013120083,0.019472204,0.048796117,0.038354214,-0.02973779,-0.09949827,0.025688775,0.009462208,-0.08409172,0.020006068,-0.0079516,-0.03384912,0.054919567,-0.010387827,-0.02357105,-0.0229434,0.024141189,-0.024124254,-0.049882855,-0.022272456,0.0926317,0.063738346,0.03212163,-0.0278857,0.0746899,0.066626355,0.0336808,0.07305985,0.04703121,-0.025281005,-0.06831803,0.013833632,0.009849246,0.058614943,-0.047318988,-0.003257637,-0.0023042774,0.03593114,-0.034255568,0.037013713,0.033210475,0.07436894,-0.018020082,0.011462461,-0.074406564,-0.038280573,-0.0009645966,-0.008973516,0.024662513,-0.051447194,-0.024967378,-0.020276885,-0.00064318115,0.015631424,-0.041368518,-0.027991896,-0.01666359,0.056758244,-0.1148229,0.06179094,0.042049363,0.037605155,-0.015206134,-0.0026195496,0.007153073,-0.031649582,0.023847967,0.018736186,-0.015592965,0.040421408,-0.009912153,0.03180303,0.041844673,-0.0028176259,-0.024754342,-5.2865336e-05,0.02551365,-0.029993301,-0.023443796,-0.046076976,0.03359282,0.01804816,0.020674115,0.04726285,-0.021301022,-0.102105334,-0.06752163,-0.06838629,0.026686741,0.09253093,0.030054111,0.00740737,-0.00977404,-0.052077163,0.03591895,0.057299793,-0.049053393,-0.025578111,-0.063721456,-0.0038303216,-0.005528575,-0.076813534,0.011896025,-0.038616106,0.035854094,-0.060751602,0.00089057226,-0.026033754,0.018490456,-0.01700688,-0.017116128,0.043773174,0.008743366,-0.0016245964,0.06949159,0.023640586,-0.019130314,-0.024368072,0.0062420173,-0.0010978195,0.10073338,-0.074851684,-0.0020676954,0.016742466,0.02586644,-0.036321916,0.07838414,0.026435176,0.016016578,0.059641946,0.024625657,-0.0049637775,-0.08117798,0.016573058,0.0148739265,-0.03693272,0.056912247,0.036978982,-0.06437767,-0.0060874955,0.0072848676,-0.028653791,0.004868969,0.0067331344,0.0016908129,-0.012908018,0.05686131,-0.06599577,0.0674892,-0.006122912,0.01945347,-0.030655535,0.026236229,0.023657631,-0.027091982,0.004207815,0.006909663,-0.036084805,0.03717742,0.011617687,-0.026980465,-0.00141742,-0.030597644,-0.02882239,-0.01202433,-0.0034528421,-0.03060077,-0.0028021052,0.013133763,0.06375068,0.07400507,0.0387916,0.021572202,-0.055147834,0.008982588,0.033431828,0.03858871,0.023240356,0.050961643,0.057727255,-0.038173847,0.017118404,0.015473532,0.0724209,0.004722163,-0.023029013,0.052532088,0.038917884,-0.08853014,-0.06854174,0.04732292,-0.044400573,-0.024460232,-0.04325698,0.014431355,-0.0045937398,-0.05640725,-0.044036824,0.055318717,0.0063434863,0.04252773,-0.010416946,0.003977598,0.028320966,0.022184027,-0.026201138,0.056109365,-0.01003827,0.02286458,0.057218622,-0.0015427143,-0.006605392,-0.004389915,0.025893612,0.019698491,0.02874529,-0.020460496,-0.071813524,0.0072388262,-0.027902385,-0.028126052,-0.0009176181,0.035686087,0.0053934236,0.019132955,0.025242742,-0.01238384,-0.06416331,-0.07449981,-0.0036220953,-0.012644136,0.032653157,-0.009614943,-0.004164691,0.0360943,0.07225011,0.011949491,0.0011223016,-0.035020635,-0.047515847,-0.04539207,-0.03458005,-0.04803867,-0.07098339,-0.0047767814,-0.02387767,-0.0012289013,-0.0064946623,0.01431482,0.008208949,0.008758454,-0.06490593,0.0032442545,-0.043095216,-0.027406488,-0.03011913,-0.013871367,-0.05837901,0.06986149,-0.09104931,0.020795459,0.0022442148,0.00090059935,0.004200362,0.06780064,0.013812911,0.016592968,-0.012447045,0.013241202,-0.013388155,-0.045954842,0.026045175,0.022353962,0.008622626,-0.001973125,-0.06644991,-0.012515542,0.0040478455,-0.017837757,-0.011868934,0.025654903,0.089035645,0.021271009,-0.0026713265,0.07108305,0.014007916,0.04360376,0.010078213,0.0020191872,-0.031349506,0.091265894,0.046548057,0.023508914,0.037618533,0.013442476,0.031526644,0.058930878,-0.059030067,0.023501385,0.018572459,-0.0028287622,0.026234236,-0.0015884888,-0.056860667,-0.04594125,0.002772766,-0.14981899,0.011533057,-0.027302196,-0.015090613,-0.03771971,0.034814816,0.0043500173,-0.021442903,0.03743782,0.00530043,-0.018012177,0.0054079476,0.047012545,-0.022518659,0.008923537,0.04729312,-0.01774093,-0.07821403,0.027626263,-0.020843282,0.0033689146,0.037538633,0.039873578,-0.0107378075,0.0016634869,0.026531307,0.032257147,0.03351215,0.0015152028,-0.06718184,0.008690678,-0.02165808,0.02224727,0.007840089,-0.022785285,0.03404269,-0.016795434,-0.012263397,-0.017759033,0.02379983,0.07013235,0.009701225,0.00935128,-0.00987246,0.032763235,-0.03131108,0.0046395864,-0.0028332684,-0.013261878,-0.05907269,0.00938289,0.007940237,-0.028094498,-0.0039265133,0.0346435,0.0064072376,-0.016269473,0.015093795,-0.025512608,-0.026086848,-0.02615408,0.009447504,0.023501491,-0.017969884,-0.03893192,-0.0065730144,-0.0066148606,0.008049213,-0.08157301,0.08254755,-0.029535757,-0.004683749,0.02662205,-0.0054314146,-0.014938656,-0.0021917727,0.062692866,0.016028108,0.03294235,0.042303897,0.01794982,0.056750827,0.020284966,0.049458478,-0.0143563915,-0.010103484,0.057800904,-0.0044507342,0.0013741619,0.003994376,0.059453063,-0.005713581,0.00029887585,0.03618384,-0.0061568203,0.025328292,-0.06033025,-0.019562768,-0.030811535,0.008641273,-0.027642729,0.039986208,0.004310884,0.010142679,-0.022244804,-0.008445305,0.009166917,0.017246237,0.028861409,-0.084363565,-0.024974003,-0.016613392,0.014450779,0.022416485,0.035890743,-0.024950916,0.017863942,0.031097792,0.07407177,-0.025281997,-0.0020021293,-0.0420218,-0.06026409,-0.027479764,0.0070954976,-0.036029458,-0.034886826,0.06785499,-0.05267662,-0.006669851,0.0022790304,0.0059362394,0.014550534,0.026903735,-0.023719657,-0.01759116,-0.05805122,-0.004225159,0.008045827,0.010477981,-0.0006514365,-0.016782334,-0.015302948,0.06950968,-0.04103109,-0.023363186,0.014775943,-0.0010547641,0.038787052,-0.034321606,-0.0017794454,0.08026514,-0.0067474884,0.0011038879,0.040687956,0.008977691,-0.007212869,0.019213518,-0.008531379,0.004115275,0.05351884,-0.002215062,0.000421544,0.00273816,0.0077937734,0.032303713,-0.020373654,0.04530105,0.0544568,-0.03865258,-0.026448887,-0.009543542,0.06903804,0.04496776,0.014978826,0.011302542,-0.0038806144,-0.031111764,0.058546565,0.031642176,-0.006414346,0.013687896,0.005908714,0.056219235,0.05683007,-0.018532082,-0.028941007,-0.05142425,-0.036049176,0.019438451,-0.035151295,-0.053055722,0.04395004,-0.03799624,-0.003542434,-0.009145251,-0.004163987,-0.040293127,-0.028071916,0.015165069,-0.05884996,0.05538873,0.009470665,0.024631398,-0.022907605,-0.0011687875,0.011907189,-0.003174495,-0.026807787,0.01693387,0.030326504,-0.0090496065,-0.014894846,-0.04759581,-0.048622552,0.033414982,0.023883138,0.10500295,-0.008784349,0.027134696,0.00614239,0.018992322,0.02531671,-0.03669057,-0.011511855,0.005333173,-0.003678908,-0.038072884,0.042147234,0.0072485744,-0.037681405,0.03082657,-0.033200607,0.05248876,0.0020400444,-0.018921902,0.004559076,0.011057436,-0.011083994,-0.0056805084,0.03063953,-0.018856525,-0.036842864,0.020916069,-0.011189779,-0.003719505,-0.01832031,-0.038747985,0.0038938613,-0.045038324,0.02269168,0.026878243,0.007059424,-0.015398917,-0.013846026,0.004085867,0.012830922,-0.012877102,0.019090071,0.022554291,-0.04540179,-0.016245425,0.09877551,-0.007691711,0.025318898,0.024816394,0.041645743,0.012189688,8.824056e-05,0.017389845,0.02671426,4.33563e-06,0.0037885713,-0.011944642,-0.023749782,0.011148169,0.001686264,-0.040983588,-0.029989963,-0.03029144,-0.025165625,-0.06044677,0.023124097,0.0027212622,0.038645305,-0.006540034,0.029426433,0.040147386,-0.080176875,-0.08736431,-0.04396175,-0.017657569,-0.021443939,0.037872493,0.007052396,0.016629085,-0.06062418,0.04891367,-0.009608705,0.014440395,0.028068393,0.0007587305,0.014105891,0.029614126,-0.017887259,0.002306138,-0.034636274,-0.06456724,-0.01998338,0.000606536,0.02069449,0.019485192,0.010030966,0.035176985,-0.009932322,0.03402048,-0.0002730568,-0.01003357,-0.0071863686,0.005093737,0.023372594,-0.035037473,0.015438985,7.9110316e-05,0.033693187,0.03297146,0.07016483,-0.00059808616,-0.03873086,0.030354569,-0.020242928,-0.034501255,0.031951588,-0.0066908253,-0.008943879,0.011993765,0.036112923,-0.013666626,-0.037324853,-0.007837367,-0.026185052,-0.019385848,-0.00036129417,-0.038568616,-0.043501295,-0.049372222,0.027231447,0.02035045,-0.03293725,-0.015659142,0.018065767,-0.0054850667,-0.009509768,-0.00871263,0.05696131,-0.010282509,0.018069632,0.04929747,-0.043006994,0.016297802,-0.017045734,-0.007435868,-0.0079318015,0.030915959,0.011030607,-0.016107092,-0.006647325,-0.020197716,0.059198584,0.022724148,0.07599346,-0.050723277,-0.009002372,-0.027135435,-0.024612974,-6.549941e-05,0.032399,0.04668707,-0.04424772,0.031268302,-0.05767878,0.023182355,-0.0273028,-0.047435034,-0.027997676,0.02445982,-0.08897834,-0.0027241663,0.031608075,0.0029737677,-0.015478959,0.029066503,-0.057396844,0.0031260753,-0.029356087,0.03758748,0.006733925,0.03606233,0.01629852,-0.04419844,0.0021931014,0.013180897,0.007732914,0.0145292925,-0.030556956,-0.016752485,0.0010125994,0.047452375,0.024555543,-0.03426633,-0.054002352,0.05133418,-0.08709131,0.053514756,0.05335034,-0.008195552,-0.03754383,-0.008401652,0.011676873,-0.027014555,-0.013119981,0.0334732,-0.012365168,-0.0073758857,0.057927057,-0.0048452183,-0.040082198,0.0029923986,0.026330471,0.03890921,0.012576424,-0.02421621,-0.041962363,-0.008795686,-0.07688286,0.030291464,0.03597378,0.0021955597,0.045860082,-0.014947699,-0.0024742251,-0.02798225,0.0022458648,0.030428033,-0.0769536,0.0034191706,-0.025521925,-0.043436553,-0.03436188,0.020119,0.0472036,0.0037970135]
four	[0.0111165745,0.09397343,-0.061730128,0.013359486,0.030409986,-0.026140008,0.055334374,0.056657035,-0.056595813,0.05852599,0.00891356,0.02254372,0.042645536,0.030865518,-0.020820469,-0.09376201,0.02148587,-0.002611573,-0.09121642,0.02112179,-0.0117494045,-0.027962055,0.062402204,-0.011709904,-0.019927848,-0.017196918,0.012803359,-0.017532723,-0.04242606,-0.0183497,0.10425154,0.06710239,0.025861127,-0.023635147,0.07783921,0.069405004,0.03125637,0.06173667,0.037029333,-0.013520976,-0.06553414,0.013977618,0.008682798,0.06171364,-0.038927626,-0.011779253,-0.0043395367,0.0263865,-0.02541734,0.04661695,0.025541779,0.06723261,-0.026105082,0.004054123,-0.07498024,-0.027333248,0.005790083,-0.006735369,0.026937997,-0.036551394,-0.014307676,-0.024227833,0.016551392,0.02143009,-0.03297009,-0.02742754,-0.02046723,0.056528155,-0.10773818,0.056080893,0.038161356,0.039530296,-0.01572884,0.00473406,-0.0053291083,-0.030638622,0.012595755,0.026128493,-0.012754917,0.048702154,-0.023813004,0.031128095,0.037271127,-0.020151634,-0.019968312,-0.00035425244,0.031716485,-0.04109973,-0.01888111,-0.035260048,0.04079279,0.015998147,0.025126183,0.04631975,-0.015596106,-0.107032314,-0.07449117,-0.06503362,0.026116112,0.09220725,0.027021714,-0.004662873,-0.011360704,-0.037820805,0.043271765,0.055079482,-0.041623935,-0.023033625,-0.042585585,-0.00090050854,-0.010264066,-0.081869304,0.015945489,-0.042868737,0.038014438,-0.07571662,-0.0011018692,-0.018179506,0.029044695,-0.0026130052,-0.020127531,0.05737579,0.00716915,-0.0077720624,0.038262088,0.04361559,-0.0115138395,-0.02400515,0.0077865627,-0.011574449,0.09717191,-0.068194516,0.0056343125,0.015146482,0.023473743,-0.037511498,0.074215196,0.028677111,0.017531274,0.06490909,0.023643317,-0.0075878673,-0.06404971,0.0043830853,0.0039210734,-0.038149264,0.05564239,0.042316746,-0.05990259,-0.011731682,-0.004315153,-0.028089708,0.012422227,0.0045900624,-0.003575891,-0.026949324,0.07129717,-0.07306966,0.065911025,-0.007842101,0.010810561,-0.045856565,0.027831193,0.037027378,-0.03660822,0.008287813,-0.005758314,-0.04835276,0.034660205,0.017495455,-0.01757062,0.0049685175,-0.02113842,-0.029801324,-0.023922445,-0.0063281124,-0.030938625,-0.014474981,0.021765495,0.058148626,0.07656864,0.0369669,0.027753826,-0.04096358,0.020357365,0.033477794,0.038722616,0.020270877,0.038832683,0.06329026,-0.036290716,0.0063139917,0.025579285,0.091166586,0.011326457,-0.02104869,0.06486711,0.04602567,-0.05926754,-0.08085099,0.047691118,-0.056904007,-0.027744105,-0.031575393,0.011004601,-0.011520502,-0.054728255,-0.04127715,0.05386834,0.011099336,0.042737644,-0.020536713,0.0041400613,0.02822529,0.03336439,-0.025691183,0.05684539,-0.0045936834,0.030473948,0.069629565,0.01058401,-0.010722157,0.0058144904,0.01928905,0.018041043,0.028421618,-0.026712202,-0.061807957,-0.0043925527,-0.018357985,-0.018409954,-0.0061935843,0.030199636,-0.013632968,0.02450328,0.023606248,-0.0077960542,-0.060704224,-0.0817072,-0.008363555,-0.009830269,0.023388937,-0.0026164402,0.0007402338,0.046562426,0.062232826,0.010008483,0.011057689,-0.040166773,-0.052217152,-0.038976282,-0.022548145,-0.049817212,-0.07111507,-0.00056681165,-0.022877192,-0.005878914,-0.0005880095,0.0040633082,0.0050012446,0.013961631,-0.059235726,0.0102008255,-0.0409802,-0.020666337,-0.03214173,-0.0016321499,-0.05930209,0.07082015,-0.09564474,0.033340577,0.0038436896,0.006755489,-0.0043181884,0.06761176,0.00626792,0.0125170825,-0.01201381,0.015562636,-0.015599189,-0.047337987,0.014134613,0.01433477,0.011713566,0.0009210865,-0.07752997,-0.008329449,-0.012963634,-0.020156952,-0.010413528,0.027275419,0.10328116,0.014196341,0.0065789334,0.06139137,0.014956414,0.03601049,0.00075954874,0.015286105,-0.02934275,0.10090577,0.059221637,0.019433998,0.02718356,0.026918761,0.03349044,0.05188921,-0.0538971,0.012125942,0.01311356,0.003113693,0.027389172,0.0094087655,-0.05466014,-0.042258117,-0.0021287058,-0.13168162,0.013316356,-0.017238153,-0.021968056,-0.03693685,0.038455937,0.006554441,-0.0058628367,0.03880976,0.00032845337,-0.00707697,-0.0006835452,0.042963214,-0.012523306,0.003018065,0.054993574,-0.018304313,-0.0853978,0.026418522,-0.019497138,0.0028488135,0.03219189,0.031650927,-0.017404996,0.00299031,0.016399633,0.029299466,0.042933337,-0.0024222664,-0.05857598,0.012805874,-0.02899068,0.019501885,0.00966831,-0.032098573,0.023941586,-0.010398586,0.0023078478,-0.020676043,0.020649036,0.07022984,0.009746938,0.010186804,-0.009893764,0.03093902,-0.026593389,0.008797323,-0.00903709,-0.012049451,-0.054227524,0.0113435555,0.007767732,-0.025443302,-0.0075673303,0.023376716,0.014013961,-0.024759535,0.006699163,-0.02831999,-0.031287894,-0.029621424,0.010823762,0.04355568,-0.0030875215,-0.03645533,-0.0028137325,-0.0016299721,0.004491292,-0.07843726,0.0832369,-0.028173028,-0.0074990275,0.016650658,0.0024417434,-0.011176611,4.927953e-05,0.054828525,0.015033568,0.028330566,0.051034346,0.020863712,0.058075596,0.024511795,0.061650693,-0.016456025,-0.0034944941,0.05555913,0.0010061038,-0.007507681,0.011984728,0.06465864,-0.0072649266,0.0027448602,0.017652826,-0.010667442,0.027190737,-0.0584036,-0.013439856,-0.023058403,-0.0053075217,-0.028065432,0.045735978,-0.012182989,0.014036117,-0.015496768,-0.013935042,0.00014192026,0.021430379,0.03644291,-0.08635623,-0.018003127,-0.00833984,0.0164762,0.012436172,0.038855,-0.029833749,0.006866159,0.029582692,0.06793069,-0.0065534813,0.0048627425,-0.040506437,-0.05172792,-0.021948993,0.018085346,-0.04335727,-0.03177267,0.070732474,-0.054296643,0.005562208,0.0010522411,0.0038822375,0.016608851,0.031615846,-0.03201291,0.0032191386,-0.066212006,-0.009457364,0.007011702,0.008719677,-0.007689021,-0.020420695,-0.010973268,0.06414404,-0.0510966,-0.040982526,0.011107973,0.010099196,0.054275617,-0.035320353,-0.009782756,0.082097836,-0.002942141,0.006347448,0.04879232,0.014070747,-0.02118203,0.016733509,-0.0080293985,0.005107638,0.042359665,0.00070973276,0.007998786,-0.0016024964,0.009557014,0.035774477,-0.008644052,0.047244143,0.040948708,-0.03684245,-0.018952195,-0.0069225905,0.075866625,0.032702032,0.026705172,0.011244127,0.0022769263,-0.043155737,0.062112857,0.03440436,-0.01685731,0.017194262,0.005724333,0.053415846,0.07095306,-0.009650908,-0.024856262,-0.046619974,-0.034100343,0.020214887,-0.04534134,-0.045163713,0.037395924,-0.020882895,-0.006324885,-0.009578559,-0.0064640795,-0.034639716,-0.021027157,0.021922465,-0.043411184,0.063123554,0.010940368,0.02327065,-0.035485264,0.004660784,0.019803638,0.013391125,-0.02414034,0.0007359468,0.038187094,-0.0018888548,-0.023095809,-0.050870083,-0.05159696,0.032983065,0.018298056,0.09770508,-0.0033543932,0.023333052,0.009750834,0.009363593,0.03042429,-0.033132527,-0.0231474,0.0064345594,0.006960268,-0.029279068,0.04894863,0.006433593,-0.02968577,0.021049649,-0.027400868,0.05385755,0.0058841966,-0.02884793,0.006390494,0.01668465,-0.01504612,-0.005469038,0.021162326,-0.034111608,-0.024955207,0.026235245,-0.013366516,-0.0043732314,-0.012255499,-0.02521984,-0.016915359,-0.031692196,0.02424312,0.039693233,0.009761326,-0.004791734,-0.017079689,0.0060959724,0.019720629,-0.033100408,0.022146452,0.028287329,-0.04892534,-0.021698233,0.10967396,-0.018023036,0.03460697,0.017969413,0.03681721,-0.0057791853,0.024659883,0.022991957,0.028121093,-0.009148762,0.0009907638,-0.030131068,-0.029616408,0.013316372,0.008657456,-0.026909046,-0.044463344,-0.026763592,-0.017969856,-0.05745097,0.031809937,0.007746641,0.03529197,-0.0075930124,0.019882347,0.041725747,-0.0654,-0.08223486,-0.029836023,-0.020878972,-0.022747127,0.04799598,-0.0072963587,0.011870586,-0.04849424,0.051110107,-0.0133752255,0.007906219,0.03883398,-0.0047690235,0.021998389,0.033204112,-0.01272468,0.01533301,-0.029080225,-0.068392195,-0.009291604,-0.011766899,0.006991604,0.021573689,-0.00097557646,0.042742725,0.00334953,0.02781498,-0.0081342915,0.0015545605,-0.010059667,0.0061641643,0.016074706,-0.038752723,0.013436994,-0.012908025,0.032236714,0.049515687,0.060896724,0.010626272,-0.046574477,0.023869038,-0.016380023,-0.03151979,0.02325454,-0.0058332714,-0.016481437,0.003527039,0.042389087,-0.009148376,-0.029439619,-0.014850639,-0.017796636,-0.031760715,0.004993184,-0.049010564,-0.0545773,-0.026021147,0.03618902,0.018447941,-0.033158433,-0.024995381,0.023930585,-0.009273118,-0.012936633,-0.01176473,0.06405406,-0.009947727,0.012240669,0.05548876,-0.037473056,0.024490802,-0.0095000435,-0.007758281,-0.000660685,0.025822729,0.0052969917,-0.01296823,-0.017177239,-0.021649309,0.05633301,0.03819541,0.0890314,-0.045290403,-0.0004976702,-0.035806887,-0.014209396,-0.0008366513,0.019658117,0.044681422,-0.04041077,0.02768459,-0.0678905,0.032885864,-0.02469403,-0.05695769,-0.019642862,0.027475942,-0.08014085,0.0010873757,0.03643052,-0.008492534,-0.014073276,0.029151484,-0.06330896,-0.006003603,-0.029478032,0.04294187,0.0047401693,0.0281597,0.0056449957,-0.04623196,0.007302542,0.018251492,0.0154994605,0.02177376,-0.028209375,-0.012939281,0.0071650334,0.038712613,0.030278424,-0.022650603,-0.05475529,0.06569408,-0.08092342,0.04963348,0.061108306,-0.003241565,-0.037370756,-0.008062607,0.010377263,-0.022085762,-0.013370069,0.026916532,-0.021793628,-0.010716598,0.054207418,-0.0037678785,-0.03085238,0.027258163,0.018490357,0.03775853,0.011620102,-0.03291236,-0.040361527,0.014981685,-0.08328905,0.03304301,0.029304532,-0.0035607761,0.037831824,-0.0054629105,0.0011293326,-0.024373682,-0.002954551,0.03241292,-0.060684096,-0.0008918517,-0.03282046,-0.034734096,-0.04791318,0.023529077,0.046940945,-0.0077540562]
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
-- Data for Name: followers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.followers (id, media_name, adult) FROM stdin;
1	surviver1000	t
3	makeuptutorial	f
2	surviver1000	t
3	princess	t
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
-- Data for Name: influencersclickspublication_clicksclicks_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.influencersclickspublication_clicksclicks_table (word, synonym) FROM stdin;
1000 thousand	1000000
1000 thousand	10^6
1 million	1000000
1 million	10^6
one thousand	1000
\.


--
-- Data for Name: influencersmedia_namefollowersmedia_name_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.influencersmedia_namefollowersmedia_name_table (word, synonym) FROM stdin;
makeuptutorial	makeuptutorial
surviver1000	surviver1000
surviver1000	surviver1000
princess	princess
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
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (movie, category, rating) FROM stdin;
Raiders of the Lost Arc	action	4/5
The Shawshank Redemption	thriller	3/5
Wings of Desire	fantasy	4/5
Amélie	comedy	5/5
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
-- Data for Name: moviesmoviemovies_personalmovie_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.moviesmoviemovies_personalmovie_table (word, synonym) FROM stdin;
The Shawshank Redemption	Die Flucht aus Shawshank
Wings of Desire	Der Himmel über Berlin
Amélie	Die fabelhafte Welt der Amélie
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
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.players (id, name, born) FROM stdin;
1	Juan	20.02.2003
2	Paul	18.04.1968
3	Xi	January 1986
4	Michael	18.01.1997
\.


--
-- Data for Name: publication_clicks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publication_clicks (publication, clicks) FROM stdin;
17.01.2011	1000000
08.03.2016	500
22.11.2014	10^6
24.12.2022	1000
\.


--
-- Data for Name: shareowner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shareowner (id, name, shares) FROM stdin;
3	Diego	15
4	Marcel	11
1	Pierre	20
2	Vladi	10
\.


--
-- Data for Name: shareowner1row; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shareowner1row (id, name, shares) FROM stdin;
1	Pierre	20
\.


--
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.songs (id, album_id, song_name, duration) FROM stdin;
1	1	Delicate	3:52
2	2	New Year’s Day	3:55
\.


--
-- Data for Name: state_capitol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.state_capitol (name, capitol) FROM stdin;
DE	Dover
HI	Honolulu
TX	Austin
MA	Boston
MD	Annapolis
IA	Des Moines
ME	Augusta
ID	Boise
MI	Lansing
UT	Salt Lake City
MN	Saint Paul
MO	Jefferson City
IL	Springfield
IN	Indianapolis
MS	Jackson
MT	Helena
AK	Juneau
AL	Montgomery
VA	Richmond
AR	Little Rock
NC	Raleigh
ND	Bismarck
NE	Lincoln
RI	Providence
AZ	Phoenix
NH	Concord
NJ	Trenton
VT	Montpelier
NM	Santa Fe
FL	Tallahassee
NV	Carson City
WA	Olympia
NY	Albany
SC	Columbia
SD	Pierre
WI	Madison
OH	Columbus
GA	Atlanta
OK	Oklahoma City
CA	Sacramento
WV	Charleston
WY	Cheyenne
OR	Salem
KS	Topeka
CO	Denver
KY	Frankfort
CT	Hartford
PA	Harrisburg
LA	Baton Rouge
TN	Nashville
\.


--
-- Data for Name: state_capitol_short; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.state_capitol_short (name, capitol) FROM stdin;
DE	Dover
AK	Juneau
AL	Montgomery
AR	Little Rock
AZ	Phoenix
FL	Tallahassee
GA	Atlanta
CA	Sacramento
CO	Denver
CT	Hartford
\.


--
-- Data for Name: state_trans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.state_trans (state_abrev, state) FROM stdin;
AL	Alabama
AK	Alaska
AZ	Arizona
AR	Arkansas
CA	California
CO	Colorado
CT	Connecticut
DE	Delaware
FL	Florida
GA	Georgia
HI	Hawaii
ID	Idaho
IL	Illinois
IN	Indiana
IA	Iowa
KS	Kansas
KY	Kentucky
LA	Louisiana
ME	Maine
MD	Maryland
MA	Massachusetts
MI	Michigan
MN	Minnesota
MS	Mississippi
MO	Missouri
MT	Montana
NE	Nebraska
NV	Nevada
NH	New Hampshire
NJ	New Jersey
NM	New Mexico
NY	New York
NC	North Carolina
ND	North Dakota
OH	Ohio
OK	Oklahoma
OR	Oregon
PA	Pennsylvania
RI	Rhode Island
SC	South Carolina
SD	South Dakota
TN	Tennessee
TX	Texas
UT	Utah
VT	Vermont
VA	Virginia
WA	Washington
WV	West Virginia
WI	Wisconsin
WY	Wyoming
\.


--
-- Data for Name: state_trans_short; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.state_trans_short (state_abrev, state) FROM stdin;
AL	Alabama
AK	Alaska
AZ	Arizona
AR	Arkansas
CA	California
CO	Colorado
CT	Connecticut
DE	Delaware
FL	Florida
GA	Georgia
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.states (name, population) FROM stdin;
North Carolina	10488084
Indiana	6732212
Wyoming	578759
Utah	3323971
Arizona	7278717
Montana	1103311
Kentucky	4467673
California	39512223
Kansas	2913314
Delaware	989948
Florida	21478738
Pennsylvania	12801989
Iowa	3155070
Mississippi	2961279
Illinois	12671821
Texas	29189580
Connecticut	3565287
Georgia	10617423
Maryland	6045680
Virginia	8600467
Idaho	1881201
Oregon	4237256
Vermont	623989
Maine	1344212
Oklahoma	3923561
Tennessee	6910818
Alabama	4903185
Arkansas	3017804
South Carolina	5148714
Washington	7701186
Nebraska	1934408
West Virginia	1792147
Colorado	5758736
Massachusetts	6949503
Missouri	6154913
Alaska	733391
North Dakota	762062
Wisconsin	5822434
Nevada	3080156
New York	19453561
Rhode Island	1059361
Hawaii	1415872
South Dakota	884659
Minnesota	5639615
New Jersey	8882190
Michigan	9986857
New Mexico	2096829
New Hampshire	1359711
Louisiana	4648794
Ohio	11689473
\.


--
-- Data for Name: states_short; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.states_short (name, population) FROM stdin;
Alabama	4903185
Alaska	733391
Arizona	7278717
Arkansas	3017804
California	39512223
Colorado	5758736
Connecticut	3565287
Delaware	989948
Florida	21478738
Georgia	10617423
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
-- Data for Name: totalanimal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.totalanimal (name, category) FROM stdin;
bill	chien
diego	chat
\.


--
-- Data for Name: totalshares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.totalshares (name, shares) FROM stdin;
Felix	20
Vladi	10
Max	9
Hans	23
\.


--
-- Data for Name: tournaments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tournaments (winner_id, name, price_money_in_million) FROM stdin;
4	Berlin Open	4
3	Warsaw Open	3
2	Jakarta Open	1.5
3	Osaka Open	0.5
\.


--
-- Data for Name: translation_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.translation_table (word, synonym) FROM stdin;
dog	chien
dog	perro
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
-- Data for Name: weatherdatewebsite_visitsdate_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weatherdatewebsite_visitsdate_table (word, synonym) FROM stdin;
2023 10 26	2023 October 26
2023 10 26	2023 October 26
2023 10 27	2023 October 27
2023 10 27	2023 October 27
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
-- Data for Name: whereanimalownercategorydog_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.whereanimalownercategorydog_table (word, synonym) FROM stdin;
dog	chien
dog	chat
\.


--
-- Data for Name: whereanimalownercategorydogoranimalownercategoryisnull_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.whereanimalownercategorydogoranimalownercategoryisnull_table (word, synonym) FROM stdin;
dog	chien
dog	chat
\.


--
-- Data for Name: whereanimalownercategoryisnulloranimalownercategorydog_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.whereanimalownercategoryisnulloranimalownercategorydog_table (word, synonym) FROM stdin;
dog	chien
dog	chat
\.


--
-- Data for Name: wherebakery_salesquantity55_comparison_55_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wherebakery_salesquantity55_comparison_55_table (word, synonym) FROM stdin;
55	5 dozen
\.


--
-- Data for Name: wherechildren_tablechildren1_comparison_1_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wherechildren_tablechildren1_comparison_1_table (word, synonym) FROM stdin;
1	4
1	many
1	2
\.


--
-- Data for Name: wheredoctorsnamepeteranddoctorspatients_pd12_comparison_12_tabl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wheredoctorsnamepeteranddoctorspatients_pd12_comparison_12_tabl (word, synonym) FROM stdin;
12	fourty
12	44
12	ten
12	11
\.


--
-- Data for Name: wheredoctorsnamepeteranddoctorspatients_pd12_comparison_peter_t; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wheredoctorsnamepeteranddoctorspatients_pd12_comparison_peter_t (word, synonym) FROM stdin;
Peter	Hans
Peter	Peter
\.


--
-- Data for Name: wheredoctorsnamepeteranddoctorspatients_pd12_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wheredoctorsnamepeteranddoctorspatients_pd12_table (word, synonym) FROM stdin;
12	fourty
12	ten
12	11
\.


--
-- Data for Name: wheredoctorspatients_pd12_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wheredoctorspatients_pd12_table (word, synonym) FROM stdin;
12	fourty
12	ten
12	11
\.


--
-- Data for Name: whereinfluencersclicks500_comparison_500_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.whereinfluencersclicks500_comparison_500_table (word, synonym) FROM stdin;
500	1000 thousand
500	1 million
500	one thousand
\.


--
-- Data for Name: wheremovies_personalpersonal_rating70_comparison_70_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wheremovies_personalpersonal_rating70_comparison_70_table (word, synonym) FROM stdin;
70%	3/5
70%	5/5
70%	4/5
\.


--
-- Data for Name: whereoven_temperaturetemperature200°c_comparison_200°c_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."whereoven_temperaturetemperature200°c_comparison_200°c_table" (word, synonym) FROM stdin;
200 °C	200 °F
\.


--
-- Data for Name: wheretennis_playersbornjanuary_comparison_january_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wheretennis_playersbornjanuary_comparison_january_table (word, synonym) FROM stdin;
January	January 1986
January	18.01.1997
\.


--
-- Name: albums album_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT album_pkey PRIMARY KEY (id);


--
-- Name: animalowner1row animalowner1row_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animalowner1row
    ADD CONSTRAINT animalowner1row_pkey PRIMARY KEY (owner_id);


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
-- Name: chemical chemicals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chemical
    ADD CONSTRAINT chemicals_pkey PRIMARY KEY (name);


--
-- Name: doctors doctors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_pkey PRIMARY KEY (id);


--
-- Name: influencers influencers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.influencers
    ADD CONSTRAINT influencers_pkey PRIMARY KEY (media_name);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);


--
-- Name: shareowner1row shareowner1row_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shareowner1row
    ADD CONSTRAINT shareowner1row_pkey PRIMARY KEY (id);


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
-- Name: tennis_players tennis_players_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tennis_players
    ADD CONSTRAINT tennis_players_pkey PRIMARY KEY (id);


--
-- Name: totalanimal totalanimal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.totalanimal
    ADD CONSTRAINT totalanimal_pkey PRIMARY KEY (name);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

