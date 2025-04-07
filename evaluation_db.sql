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
-- Name: ground_truth_left; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ground_truth_left (
    aggregate text
);


ALTER TABLE public.ground_truth_left OWNER TO postgres;

--
-- Name: jio_smart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jio_smart (
    category text,
    items text
);


ALTER TABLE public.jio_smart OWNER TO postgres;

--
-- Name: left_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.left_table (
    aggregate text
);


ALTER TABLE public.left_table OWNER TO postgres;

--
-- Name: left_tableaggregateright_tableaggregate_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.left_tableaggregateright_tableaggregate_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.left_tableaggregateright_tableaggregate_table OWNER TO postgres;

--
-- Name: mercari_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mercari_data (
    name text,
    category text
);


ALTER TABLE public.mercari_data OWNER TO postgres;

--
-- Name: right_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.right_table (
    aggregate text
);


ALTER TABLE public.right_table OWNER TO postgres;

--
-- Name: wherejio_smartitemsbeauty_comparison_beauty_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wherejio_smartitemsbeauty_comparison_beauty_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wherejio_smartitemsbeauty_comparison_beauty_table OWNER TO postgres;

--
-- Name: wherejio_smartitemselectronics_comparison_electronics_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wherejio_smartitemselectronics_comparison_electronics_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wherejio_smartitemselectronics_comparison_electronics_table OWNER TO postgres;

--
-- Name: wherejio_smartitemsfashion_comparison_fashion_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wherejio_smartitemsfashion_comparison_fashion_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wherejio_smartitemsfashion_comparison_fashion_table OWNER TO postgres;

--
-- Name: wherejio_smartitemsjewellery_comparison_jewellery_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wherejio_smartitemsjewellery_comparison_jewellery_table (
    word text NOT NULL,
    synonym text NOT NULL
);


ALTER TABLE public.wherejio_smartitemsjewellery_comparison_jewellery_table OWNER TO postgres;

--
-- Data for Name: ground_truth_left; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ground_truth_left (aggregate) FROM stdin;
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
title (deluxe)\nmeghan trainor\n 2014, 2015 epic records, a division of sony music entertainment\n9-Jan-15\ncredit\n2:51
slow down (remixes)\nselena gomez\n 2013 hollywood records, inc.\n20-Aug-13\nslow down (smash mode remix)\n5:21
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
the reason - ep\nx ambassadors\n 2015 kidinakorner/interscope records\n10-Aug-15\nshining\n3:40
nick jonas\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\nnothing would be better\n4:34
nick jonas (deluxe)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48
nick jonas (deluxe)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48
nick jonas\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\nnothing would be better\n4:34
#NAME?\ned sheeran\n 2011 warner music uk limited\n9-Sep-11\nsunburn\n4:35
loose change\ned sheeran\n 2010 all tracks (p) 2010 paw print records under exclusive license to warner music uk limited except for track 1 (p) 2011paw print records under exclusive license to warner music uk limited\n9-Dec-11\nfirefly (bravado dubstep remix)\n4:29
x\ned sheeran\n 2014 asylum records uk, a warner music uk company\n20-Jun-14\nafire love\n5:14
\.


--
-- Data for Name: jio_smart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jio_smart (category, items) FROM stdin;
Beauty	Flormar Quick Dry Nail Enamel QD20 Rose Taboo 11 ml
Electronics	EPSON T7741 Ink Bottle, Black
Electronics	Venus Vector Hi Speed Ceiling Fan V1200 ( White)
Jewellery	Reliance Jewels Bal Gopal Ovel Gold 24 KT (999) 4 GM Coin
Electronics	Zebronics Zeb-Rocket Portable Bluetooth Wireless Speaker with AUX, USB, In-built FM radio
Electronics	EVM Enlarge 30000 mAh Power Bank, P0100
Beauty	mCaffeine Naked & Raw Moisturizing Coffee Body Lotion 200 ml
Jewellery	Reliance Jewels Swastik Round Gold 24 KT (999) 4 GM Coin
Electronics	Hanumex UV Protection Lens Filter (52 mm)
Beauty	Maryaj Deuce Homme EDP Spicy Woody Perfume And Ajmal Carbon Homme Deodorant Citrus Spicy Fragrance 300 ml
Fashion	MarkQues Men''s Watch and Genuine Leather Wallet Combo Gift Set for Men (BON-770909-VIN-4401)
Electronics	Viblitz Black Camera Belt
Fashion	PEACH MS-4
Beauty	O-Lens Spanish 1Day Coloured Contact Lenses - Grey ( 0.00 ) 1''s
Fashion	BownBee Boys Green Printed Cotton Blend Kurta Sets
Jewellery	Reliance Jewels Laxmi-Ganesh Gold 24 KT (999) 10 GM Coin
Electronics	Apple MU7E2ZM/A USB-C to 3.5 mm Headphone Jack Adapter
Electronics	SellZone Charger Adapter For Laptop Accer Spin 3
Electronics	SellZone Replacement Laptop Battery For Hp Pavilion Dv6-3050Tx(VIKBATTG0H01027)
Fashion	Striped Dungaree Dress
Jewellery	Reliance Jewels Shree Round Gold 24 KT 999 2 GM Coin
Jewellery	Reliance Jewels Ag 99.9 5.51 gm Lakshmi Ganesh Silver Idol
Jewellery	Reliance Jewels Shree Round Gold 24 KT (999) 4 GM Coin
Fashion	SWADESI STUFF Analogue White Dail Watch For Women- (SDS 127 $)
Beauty	Ajmal Kuro EDP Aromatic Spicy Perfume And Blu Femme EDP Floral Woody Perfume 140 ml
Fashion	GFB Women Multicolor 100 Percent Silk Printed Stoles Scarf
Fashion	Nakabh Elegant Box Linked Collection Golden Silver Dual Plated Stainless Steel Necklace Chain for Boys Men
Fashion	Hangup Men''s Blazer Polyester Viscose Regular Checkered D942ButtonBlazer
Fashion	Pearl Night Wears Womens Purple Alpine Nighty - XL
Electronics	Mycrofine Superstar Plus Chocolate Strawberry Flour Mill with Smart I-Sensor Technology, Child Safety Door Switch
Electronics	Inclu For Vivo V5 plus Waterproof, Artificial Leather, Scratch Resident, Magnetic Lock Holster Case
Electronics	SellZone Laptop Charger Adapter For Dell La65Ns2-00 65W
Beauty	Fashion Colour Normal Eyelashes 1''s
Fashion	PEKUNIARY Full Rim UV Protection Aviator Sunglasses For Men & Women - (Black lens)
Beauty	House Of Makeup Good On You Hydra Matte Lipstick - Pinkie Swear 3.5 gm
Beauty	Faces Canada Ultime Pro Longstay Liquid Matte Lipstick Ravishing Wine 18 6 gm
Fashion	ZEBU Women Multicolor Abstract 100% Cotton Pack of 2 Capris
Fashion	Memoir Silver Plated Brass Free Size Ring (Women)
Jewellery	Reliance Jewels RL 50 GM Silver (999) Coin
Fashion	Sanwara Men Green Art Silk Self Design Kurta and Pyjama Set
Beauty	Sri Sri Tattva Deva Vati 500 mg Tablet 60''s
Beauty	Maryaj M For Her EDP Fruity Floral Perfume And Maryaj Goldie EDP Fruity Floral Perfume 190 ml
Beauty	Fashion Colour Kiss Lip No Transfer Lipstick, 94 Bordeaux 2.6 gm
Fashion	HPS Sports Men Multicolor Polyester Printed Tracksuit (L)
Electronics	Kingston 64 GB USB 3.0 DataTraveler 100 Flash Drive, DT100G3
Jewellery	Reliance Jewels Bal Gopal Round Gold 24 KT (999) 4 GM Coin
Electronics	Black Product
Fashion	ORIFWSH-1238 BLACK-6
Beauty	Makeup Revolution Colour Cult Brow Palette Dark 3.2 gm
Beauty	Cadiveu Extreme Repair Shampoo Sulfate Free 300 ml
Beauty	Daily Life Forever52 Long Wear El Eyeliner & Tattoo Gt008 5 GM
Fashion	NEUTRON Brand New Style casual Brown Colour Analog Genuine Leather Belt Watch For Boys And Men - BL46.62
Fashion	Fasla Boys Multicolor Printed Pure Cotton Pack of 5 Shorts
Fashion	Kam Garments Men Navy Cotton Printed Shorts (38)
Electronics	Hanumex Umbrella Stand Setup With Sun Gun Adapter B-Bracket Set
Electronics	Oppo Enco W31 True Wireless Earbud with Dual Microphone, Noise Cancellation, Wearing Detection, Black
Electronics	U&I Purple On The Ear Zip Series Wired Headphone With Mic
Electronics	Zapcase Black Rubber Back Cover For Xiaomi Redmi 5 19.5 x 13.5 x 2 cm
Beauty	Ajmal 4 Nightingale Deo & Neea EDP Pack of 3 20 ml
Beauty	Ajmal Raindrops EDP Floral Chypre Perfume And Sacrifice For Her EDP Floral Musky Perfume 100 ml
Electronics	Hiffin Black Backdrop Support System 9Ft Support Stands Carry Bag (Set Of 1)
Electronics	Lumiford Ultimate U30 Wired Earphones with In-built Mic and Tangle Free Cable (Black)
Beauty	Ajmal Shiro EDP Citrus Spicy Perfume And Silver Shade Homme Deodorant Citrus Woody Fragrance 290 ml
Fashion	Time Up Digital Multicolor Watches For Boys And Girls (Pack Of 2)
Beauty	Ajmal Senora EDP Floral Spicy Perfume And Aurum Concentrated Perfume Oil Fruity Floral 85 ml
Electronics	Reconnect Marvel Thanos Pop Socket & Stand, Secure grip, Hands free viewing, Solid stick 3M tape, Free car mount included, Mobile Accessories- DPS101 TH
Fashion	Fourfolds Boys Green Solid Cotton Blend Kurta Set
Fashion	Girls Orange Embroidered Dress (3-4 Y)
Electronics	Sheffield Classic Black SH-1003 Barbeque Without Stand
Beauty	Ajmal Yearn & Neea EDP Pack of 2 200 ml
Electronics	Zeiss 000000-1933-987 POL Filter circular 52MM
Fashion	Elite Crafts Stylish Bird Designed Textured PU Leather Adjustable Auto-Lock Buckle Belt For Men
Beauty	Fashion Colour Kiss Lip No Transfer Lipstick, 02 Orange 2.6 gm
Fashion	Bewakoof Women Moody Printed Half Sleeve Round Neck T-Shirt
Electronics	Palfrey Electric Extension Board - 5A + 5A + 5A + 1 Universal Two Pin Socket with Master Switch and Heavy Duty 5 Meter Wire
Electronics	Amkette Xcite Pro Wired Keyboard
Electronics	boAt TWS Airdopes 381 RTL Wireless Earbuds with Up to 20 Hours of Music Playtime, Mint Purple
Beauty	Miss Rose High Blendable Blusher 7004 - 070 01 12 gm
Fashion	Hangup Men''s Blazer Polyester Regular Print D53TuxedoBlazer
Beauty	Fashion Colour Primer + Concealer 2 In 3 8.8 gm
Electronics	Gyzmofreakz Black Gorilla Tripod
Fashion	Tooba Handicraft Red Velvet Women Designer Clutch Bag With Shoulder Strap
Electronics	Battlefield 2042 PS5 Game (Standard Edition with All-New Equipment Inspired by the Near-future of 2042)
Fashion	Vaishma Women Multicolor Solid Cotton Blend Pack of 5 Panties
Fashion	G-BULL Women ORANGE Beanies Cap
Electronics	Samsung Galaxy Watch Active 2 4G Smart Watch with IP68 Water and Dust Resistant, Embedded-SIM (Black)
Electronics	Bose 700 Soundbar, Black
Electronics	Buddhu Multicolor Plastic Back Cover For Realme C3
Fashion	IndiWeaves Girls Cotton Printed Lower Pyjama/Track Pant (Pack of 6)
Electronics	Noise Classic Nylon 22 mm Smart Watch Band, Ash Grey
Fashion	Yipsy Fashion Unisex Multicolor NightSuit (Pack of 5)
Fashion	Elligator Round Sunglasses for Men and Women UV Lens Protection
Fashion	Abaranji Men White Pure Cotton Dhoti (Free)
Electronics	Black Product
Beauty	Beauty People Velvet Matte Nail Polish Matte - Me - Magenta - Haze - 1002 9.9 ml
Fashion	ROADIES RD-204-C2 SQUARE SUNGLASSES UV400 PROTECTION
Fashion	Time Up Digital Led Black Watches For Kids (Pack Of 2)
Beauty	House Of Makeup Nail Lacquer - Inferno 12 ml
Fashion	Baseball Cap with Embroidered Text
Jewellery	Reliance Jewels RL Silver (999) 25 GM Coin
Fashion	Wo ai ni Trendy Black Heels For Women
Beauty	Ajmal 2 Wisal Dhahab Deo & Yearn EDP Pack of 3 20 ml
Jewellery	Reliance Jewels Laxmi-Ganesh Silver (999) 10 GM Coin
Electronics	WIB Grey Blood CIrculation Machine Massager
Fashion	Kiddiewink Cute Kid''s Soft Velvet Animal Cartoon School Backpack Bag for Baby Boy/Girl(2-6 Years) Pack of 2
Fashion	Hmtr Analog White Dial Silver Strap Watch For Men (Hmtr-7076-White)
Fashion	On Time Octus Analog Multcolor Watch For Women (Pack Of 2)
Fashion	Ultrafit Ultima White Non Wired Non Padded Everyday Bra for Women - 44
Beauty	DeBelle Gel Nail Lacquer Toffee Rose Choco Brown Nail Polish 8 ml
Fashion	Kleat Men''s Black Synthetic leather Formal Shoes
Electronics	boAt Immortal 1300 Gaming Bluetooth Headphone, Phantom Blue
Electronics	JBL Tune 230 NC True Wireless Earbuds with Noise Cancellation, Blue
Fashion	Lewania Womens and Girls Brown Cotton Embroidery Trending Nighty
Beauty	House Of Makeup Pout Potion Liquid Matte Lipstick - Keeper 
Fashion	Aasheez Women Green Heels
Electronics	Insta360 Run Bundle-DPTPKSC/A
Jewellery	Reliance Jewels Ag 99.9 15 gm Lakshmi Ganesh Silver Idol
Jewellery	Reliance Jewels Ag 99.9 2.65 gm Lakshmi Silver Idol
Electronics	Thrifty Tech NP Mix 2000 Pro Latest Updated Super Heavy Duty Note Counting Machine
Electronics	Viblitz Black Background Accessories Kit (Pack of 26)
Beauty	Ajmal Desert Rose EDP Floral Oriental Perfume And Wisal EDP Floral Musky Perfume 150 ml
Beauty	Swati Cosmetics Coloured Lenses Sapphire 1 Month Contact Lenses ( - 2.5) 1''s
Fashion	Memoir Gold Plated Brass Pendant Yellow (Men and Women)
Beauty	Dromen & Co Magic Cotton Pads 30 Gm
Beauty	The Man Company Charcoal Soap Bar - Black 125 gm
Electronics	INDIACASE Galaxy A9 2018 Blue Shockproof,Anti-Scratch,Mirror Plating Stand Clear View Case Cover
Electronics	Fitup Black Heavy Plastic Tripod With Holder (Set Of 1)
Beauty	Blenior Wax Strips Complete Set Normal Hair 41 Pcs 1''s
Fashion	Wildhorn Men Laptop Bag
Electronics	ptron Bassbuds Vista TWS Earbud with 5W Qi Wireless Charging, Grey
Beauty	The Moms Co. Natural Vita Rich Face Cream 25 ml
Beauty	Ajmal Kuro EDP Aromatic Spicy Perfume And Khofooq Concentrated Perfume Oil Woody Oudhy 108 ml
Beauty	Ajmal Aurum EDP Fruity Floral Perfume And Bombay Dreams EDP Floral Fruity Perfume 175 ml
Electronics	Lapcare Laptop Adapter For Lenovo Ideapad G50 G50-30 G50-45 G50-70 G50-80 65W Charger(LVOADVA4334-4)
Fashion	Ramdev Art Fashion Jewellery Sterling Silver Plated Alloy Anklet for Women ,Pack of 2
Beauty	Merlion Naturals Lime Peel Powder 227 gm
Beauty	Ajmal Wisal Dhahab Carbon Deodorant Spray (Pack of 4) 200 ml
Electronics	Samsung Galaxy M02s 32 GB, 3 GB RAM, Red, Mobile Phone
Beauty	Beardo Perfume - Whisky Smoke 100 ml
Jewellery	Reliance Jewels Ag 99.9 7.43 gm Bal Krishna Silver Idol
Jewellery	Reliance Jewels Flower Round Gold 24 KT 999 1 GM Coin
Beauty	Fogg Fresh Aromatic Deo 120 Ml
Electronics	Buy Genuine Black Aluminium Tripod
Beauty	Aloe Veda Smoothing Hair Serum (Leave-On) - Grape Seed Oil 100 ml
Electronics	Xiaomi 11i 5G Hyper Charge 128 GB, 6 GB, Pacific Pearl, Mobile Phone
Beauty	Ajmal Diza EDP Fruity Floral Perfume And Oudh Mukhallat Concentrated Perfume Oil Oriental Oudhy 106 ml
Beauty	Mother Sparsh 99% Water Based Wipes (Pack of 2 x 72''s)
Jewellery	Reliance Jewels Ganesh Silver 10 GM (999) Coin
Beauty	Passion Indulge HAIR Proteinz Spa 250 gm
Electronics	Drumstone Black Gt-08 Bluetooth Smart Watch With Camera
Electronics	BROLAVIYA X3 Flexible Arm Mount Mobile Stand for 4 to 10.5 Inch Smartphones/ Tablets (Black)
Beauty	Nature''s Essence Lightening Gel Face Wash - Orange & Lime 100 ml
Electronics	Saco Transparent Keyboard Skin For ASUS ROG Strix G15(CKS-AS-461-0-T)
Fashion	Sutara Women''s Flats Slipper
Electronics	Inalsa Kardia Cordless Vacuum Cleaner with Enhanced HEPA Filter System
Beauty	Fashion Colour Lip Liner, Waterproof, Long Lasting, 11 Pinky Pie 0.35 gm
Fashion	Bacca Bucci BALANCER Men''s Fashion Sneakers Lace-Up Trainers Basketball Style Walking Shoes
Fashion	MarkQues Men''s Tan and Brown Leather Wallet & Belt Combo (AUR-2204 CL-02)
Electronics	Kelvinator 272 litres 3 Star Double Door Refrigerator, Purple Red KRF-B290PRV
Beauty	Swati Cosmetics Coloured Lenses Turquoise 6 Month Contact Lenses ( - 1.25) 1''s
Jewellery	Reliance Jewels Ag 99.9 8.5 gm Sai Baba Silver Idol
Electronics	Oppo A16e 32 GB, 3GB RAM, Midnight Black, Mobile Phone
Beauty	SUGAR Cosmetics Goddess Of Flawless SPF30+ BB Cream - 32 Cortado (Medium) 25 ml
Electronics	BenQ TK Series TK800M Home Projector
Electronics	boAt BassHeads 220 In-Ear Wired Earphones With Super Extra Bass, Metallic Finish, Tangle-Free Cable and Gold Plated Angled Jack, White
Fashion	Q-Rious Women Multicolor Solid Pack of 3 Capris
Beauty	Berina Hair Treatment Spa 1000 gm
Beauty	Berina Hair Spray- Super Firm Hold (Gold) 450 ml
Electronics	Noise Zest 3 Watts Bluetooth Speaker with Up to 8 hours of Playtime, Green
Electronics	SellZone Replacement Laptop Battery For Asus A46 A56 K56C(VIKBATTG0H01289_sbs)
Fashion	Mikado Analog Black Watch For Girls
Electronics	Prestige 16 litres Water Purifier, Tattva 2.1 with Copper Benefits and Chemical Free Purification
Electronics	Apple Watch Series 7 Cellular - 41 mm Midnight Aluminum Case with Midnight Sport Band
Fashion	Crepeon Men Multicolor Cotton Blend Solid Brief (Pack of 2) (XXL)
Beauty	SUGAR Cosmetics Citrus Got Real Daily Moisturizer 60 gm
Electronics	Maxpro Multicolour Edge To Edge Tempered Glass And PC Protective Cover 41mm - For Apple Iwatch Series 7, SE, 6, 5, 4, 3, 2 And 1 Pack of 2
Electronics	Zebronics Zeb-Max Plus V2 Mechanical Gaming Keyboard with 5 LED Speed Modes, 2 Step Stand, 4 Brightness Levels + 1 LED Off Mode
Electronics	Xiaomi 12 Pro 5G 256GB, 12GB RAM, Couture Blue, Mobile Phone
Beauty	Bourbon Spice - Hair & Beard Conditioner 250 ml
Electronics	BlueRigger SuperSpeed USB 3.0 Type A Male to Type A Male Cable - 1.8 m
Beauty	Blue Heaven Hypergel Nailpaint - Vegas Gold, 703 11 ml
Beauty	Gemblue Biocare Cucumber Face and Body Gel 500 ml
Fashion	Dubblin DB-25-MILITARY Stylish Multipurpose Backpack
Fashion	Talgo Analog Round Grey Dial Black Leather Strap Wrist Watch for Men & Boys, Pack of 1 - LR47
Beauty	Aloe Veda Clarifying Herbal Face Wash - Turmeric 100 ml
Electronics	Reconnect Marvel Iron ManWired Headphone specially Crafted for children, 40mm speaker driver, Soft sound qulaity, Sensitivity limited upto 85db, compatible with Siri/Alexa/GoogleOk - DWH101 IM
Electronics	Redmi Note 11s 128 GB, 6 GB RAM, Space Black, Mobile Phone
Electronics	VITEK VT-2316 B-I Hair Dryer Compact High Power Travel, Mini Hair Dryer With Foldable Handle, 1800 Watt Hair Dryer Machine -Blue
Beauty	Faces Canada Ultime Pro Longstay Liquid Matte Lipstick Sultry Rogue 13 6 Ml
Fashion	MATRIX Day & Date Analog Gold Plated Wrist Watch for Men & Boys (Gold)
Electronics	Samsung 108cm (43 inch) Full HD LED TV - UA43T5310AKXXL
Fashion	Esprit Analog Rose Gold Watch For Women (Es1L268M0065)
Beauty	Beauty People Smart Nails - All That Jazz 3 - D Nail Polish Jazz - Me - Blue - 1030 12 ml
Fashion	Men''s Suede Jutti''s, Nagra''s and Mojari''s
Electronics	Apple iPad Mini 6 2021 21.08 cm (8.3 inch) Wi-Fi + Cellular Tablet, 64 GB, Space Grey, MK893HN/A
Electronics	Realme Buds Q2 Neo Earbuds with Instant Connection, IPX4 Sweat and Water Resistant, Black
Fashion	Women Black Polyester Blend Solid Capri (M) 
Jewellery	Reliance Jewels Ag 99.9 8.5 gm Hanuman Silver Idol
Electronics	Redgear Manta MT21 Gaming Keyboard and Gaming Mouse Combo (Black)
Fashion	Time Up Digital Multicolor Watch For Boys And Girls (Pack Of 2)
Electronics	NOVA NHT 1038 Trimmer for Men
Electronics	Zapcase Black Rubber Back Cover For Vivo Y83 Pro 19.5 x 13.5 x 2 cm
Fashion	University Trendz Men Leather Bracelet Set (Pack of 4)
Beauty	Biosoft Wax Strips Roll Essentials 100''s
Fashion	Vighnaharta Rhodium Alloy 12 Ring (Women And Girls)
Beauty	Revolution Pro New Neutral Satin Matte Lipstick Thirst 3.2 gm
Electronics	Beats Flex Wireless Bluetooth Earphone, Black
Electronics	Reconnect Marvel Captain On ear foldable Wireless Headphone with built in mic & Siri/Alexa/GoogleOk compatible, 10hrs playtime, Super hero Design - DBTH301 CM
Beauty	Maryaj Pebble Style EDP Spicy Woody Perfume And Ajmal Evoke Silver Edition Him Deodorant Spicy Floral Fragrance 300 ml
Fashion	Chris & Kate Polyester 21 LTR Brown Spacious Comfort Casual Backpack|Laptop Bag|School Bag|College Bag
Fashion	Okos Gold Plated Lucky Charm Delicate Tortoise Rakshabandhan Alloy Rakhi Bracelet With White Meenakari And Artificial Beads For Loving Bhai/Bhaiya/Brother RK1000396
Beauty	Gemblue Biocare Charcoal Massage Gel 500 ml
Beauty	Ajmal Wisal & Silver Shade & Sacrificeiihim & Raindropss Deo & Ascend EDP Pack of 5 20 ml
Electronics	Samsung 60.96 cm (24 Inch) LED Flat Computer Monitor with VA Panel (Black)
Beauty	NOTE NAIL ENAMEL 46 9 ml
Fashion	Romaisa Women''s Satin Solid Regular Length Pajama Top and Jumpsuit (Free Size) (Pack of 3) (PJ105-261)
Beauty	Quench Botanics Mama Cica Oil Control Overnight Mask 50 ml
Jewellery	Reliance Jewels Laxmi Gold 24 KT (999) 2 GM Coin
Fashion	Cocco Berry Unisex Multicolor Pure Cotton Shirt (M)
Fashion	Abaranji Men White Pure Cotton Dhoti (Free)
Electronics	Mobi Elite Multicolor Plastic Back Cover For Vivo V11
Fashion	Hamt Analog Brown Watch For Men (Ht-Gr010-Brown)
Electronics	Hiffin Black DSLR Camera Lens Reversal Macro Reversing Ring
Electronics	INDIACASE OnePlus 6T Black Translucent, Shockproof, Hard Back Cover
Jewellery	Reliance Jewels Ag 99.9 6.63 gm Lakshmi Silver Idol
Electronics	Hiffin Yellow 9Ft Background Stand Top Pipe Yellow Backdrop 8X12Ft 7Ft Light Stand Ring Light Bag (Set Of 1)
Fashion	HANGUP Men 3Pc Kurta Pyjama and Indo Black PolyBlend 3pc_S46KahkhiSilkKP
Electronics	SellZone Laptop Charger Adapter For Accer Aspire V5-572G
Beauty	Miss Claire Eyebrow Stix - Brown 1.14 Gm
Fashion	DIAZ Boys Printed Pure Cotton T Shirt (Pack of 3)
Beauty	Maybelline New York Instant Age Rewind Concealer, Sand-122/6ml
Fashion	Abaranji Men White Purple Pure Cotton Dhoti (Free)
Fashion	In Care Lingerie Women Cotton Blend rt Multicol Boy Sho Panties (Pack of 3)
Electronics	Apple iMac 60.96 cm (24-inch) All-In-One Desktop (8-core Apple M1 chip/8 GB/256 GB), MGPM3HN/A Pink
Beauty	Revolution Wild Animal Fierce Palette 18 gm
Fashion	BownBee Girls Pink Printed Cotton Blend NightSuit
Fashion	Cup’s-In Black Self Design Cotton Pack of 2 Bra Extender
Beauty	Dot & Key Glow-C Sleep Mask 60 ml
Fashion	Silver Shine Gold-Plated Alloy Mangalsutra (Women)
Fashion	Birde Sports Shoes
Fashion	IDEE Women Gradient Butterfly Pink Sunglasses
Electronics	Reconnect 20000 mAh Power Bank, RAPBB2001
Jewellery	Reliance Jewels Ag 99.9 5.85 gm Ganesha Silver Idol
Electronics	RiaTech Black Gaming Mouse Pad(Green Border Mouse Pad-5Pack)
Electronics	DIGISOL DG-GR6010 Wireless Router with 1 PON and 1 Gigabit LAN Port
Electronics	Bang & Olufsen Beoplay H4 2nd Gen Wireless Bluetooth Headphone with Google Assistant, Up to 19 Hours of Playtime, Limestone
Electronics	Zapcase Black Rubber Back Cover For Motorola Moto G40 Fusion - Motorola Moto G60 19.5 x 13.5 x 2 cm
Electronics	Sandisk Ultra 16 GB microSDHC Memory Card
Beauty	Bio Margosa Shampoo & Conditioner 120 Ml
Electronics	Techlife Solutions Black Plastic, Metal Tripod
Fashion	Time Up Digital Grey Watch For Boys And Girls
Beauty	Glimmer Premium Nail Enamel Ruby Red 10 ml
Beauty	Sery Colorflirt Nail Paint Fire Orange 10 ml
Electronics	Bajaj Ivora Mixer Grinder
Jewellery	Reliance Jewels Laxmi Silver (999) 10 GM Coin
Jewellery	Reliance Jewels Mahavir Ji Round Gold 24 KT 999 2 GM Coin
Electronics	Lumiford GoMusic BT12 True Wireless Portable Wireless Speaker with IPX4-Splash Proof, Voice Assistance and Multi connectivity Options (Black)
Electronics	Oddy PSCC-H8S Cross Cut 8 Sheets Paper Shredder For Home, Office And Heavy Duty Usage
Electronics	Pantum Multi-function Laser Printer, M7102DN (Toner Cartridge)
Jewellery	Reliance Jewels 5 GM 24KT Gold Coin
Fashion	Pokory Boys Pink Printed 100% Cotton Single Nightsuit
Beauty	The Moms Co. Natural Age Control Under Eye Cream 25 gm
Fashion	SN-16
Fashion	IndiWeaves Girls Cotton Printed Lower Pyjama/Track Pant (Pack of 4)
Beauty	Ajmal Jannatul Firdaus & Majmuah Of CP & Ascend EDP Pack of 3 20 ml
Beauty	Nicka K NINE COLOR Eyeshadow PALETTE - BIRTHDAY CAKE 11.7 gm
Beauty	Ajmal 1 Shadow Homme, 1 Wisal Dhahab, 1 Magnetize And 1 Persuade Deodorants Pack of 4 200 ml
Electronics	Fitup Black Gorilla Tripod With Holder (Set Of 1)
Fashion	DIAZ Boys Printed Pure Cotton Track Pants (Pack of 3)
Fashion	LOF Round Designer Sunglasses For Women Leopard Color Frame UV Protection Latest And Stylish (LS-D1712-C4I52I Brown Color Lens)
Beauty	Revolution Skincare Hydro Bank Hydrating Sleeping Mask 50 ml
Fashion	Ragzo Men Brown Slim Jeans
Fashion	Wildhorn Men Laptop Bag
Fashion	Gansta Uv Protection Gradient Over-Sized Full-Frame Brown Sunglasses ,Women(GN1055-DA-Brn)
Fashion	Tees World Women Yellow Regular Fit Round Neck Pure Cotton Tshirt
Beauty	Vega Set Of 20 Brushes (LK - 20) 740.4 gm
Beauty	Charmacy Milano Stunning Longstay Liquid Lip (Love Punch) 5.6 ml
Beauty	I Am Eyeconic Matte Neon Pure Pigments VOILET VOLTAGE 2 gm
Beauty	Police Passion Femme Deodorant Spray 200 ml
Fashion	Nakabh Elegant Bold Statement Collection Gold Silver Plated Dual Tone Stainless Steel Necklace Chain for Boys Men
Fashion	Moon walk Black Fashionable Bellies for Women
Fashion	NEUTRON Classical Rich army digital sports Blue Colour Digital Resin Belt Watch For Boys And Men - BC16
Electronics	FOUR STAR FST-1022 Waterproof 12 trim settings Cordless Trimmer for Men, Black
Fashion	A.T.U.N. Girls Mint Full Sleeve Lace Dress
Beauty	Gemblue Biocare Cucumber Face and Body Scrub 500 ml
Electronics	Dulcet DC-2020X Car Stereo
Fashion	Women Nighty with Robe (Blue)
Beauty	Nicka K RADIANT LIQUID SHADOW- GOLD LAVA 5 gm
Beauty	Miss Claire Glimmersticks For Eyes E-12 Deep Brown 1.8 Gm
Electronics	HP DeskJet 2676 Inkjet Multifunction Colour Wi-Fi Printer
Jewellery	Reliance Jewels OM Round Gold 24 KT 999 2 GM Coin
Fashion	Leaderachi Men Leather Black Brown Wallet With Key Ring And Pen (Haleatherswkp-618Bk)
Electronics	Neopack Laptop Svelte Sleeve for 33.78 cm (13.3 inch) Macbook, Midnight Blue
Electronics	U&I Neon In The Ear Sixer Series Trending 12 Hours Battery Backup Bluetooth Headset
Beauty	Miss Claire Pearl Eyeliner - 15 - Black Blue 5 Gm
Fashion	WIN9 Men Blue Striped Sneakers Outdoor Casual Lifestyle Shoes
Beauty	Belora Paris World Matte Vit C Popsicles - 013 Earthy Sudan 4.2 gm
Electronics	Xiaomi Redmi 10 Prime 128 GB, 6 GB RAM, Bifrost Blue Mobile Phone
Fashion	SCATCHITE Boys Multicolor Colorblock 100% Cotton T-shirt
Jewellery	Reliance Jewels RL Silver (999) 100 GM Coin
Beauty	Ajmal Raindrops EDP Floral Chypre Perfume And Amber Magic EDP Spicy Aromatic Perfume 150 ml
Beauty	Ajmal Nightingale & Distraction & Magnetize & Persuade Deo & Aretha EDP Pack of 3 20 ml
Jewellery	Reliance Jewels Ag 99.9 8.73 gm Lakshmi Ganesh Saraswati Silver Idol
Electronics	Redmi Note 10 Pro Max 128 GB, 8 GB RAM, Vintage Bronze, Mobile Phone
Electronics	OPPO A76 128 GB, 6 GB RAM, Glowing Black, Mobile Phone
Electronics	Resonate RouterUPS CRU 12V3A & MVC Splitter Power back up Mini UPS for 3 Devices
Fashion	Looper Printed Shorts with Insert Pockets
Fashion	Laheja Women Multicolor3 Floral Georgette Single Saree
Fashion	Kid''s fancy denim and cotton dungaree suits
Electronics	Urbn 20000 mAh Ultra Compact 22.5W Power Bank with Quick Charge and Power Delivery Compatible (Blue)
Electronics	Hiffin Green 9Ft Stand Top Pipe Clips Curtains 6X10Ft E27 Single Holder Umbrella 20W Bulb Carry Bag (Set Of 1)
Fashion	Abaranji Men White Green Solid Pure Cotton Dhoti (Free)
Beauty	Revolution Pro New Neutrals Smoked Shadow Palette 18 gm
Beauty	Rejuvenating UBTAN Lip Balm - Vanilla 5 gm
Fashion	Cotton Shirt with Patch Pocket
Beauty	Insight Cosmetics Concealer Foundation - Soft Honey 20 ml
Fashion	Pro-Ethic Style Developer Kid''s Silk Lemon Kurta Pajama Set For Boys
Beauty	Flormar Glitter Nail Enamel GL02 Pink Silver 11 ml
Fashion	Papio Digital Black Dial Pink Strap Watch For Girls And Boys
Electronics	Wearfit SPO2 and Body Temperature Tracker Inch Black Health Plus Pro Smart Bracelet For Unisex
Jewellery	Reliance Jewels Laxmi-Ganesh Gold 24 KT (999) 5 GM Coin
Beauty	Bonjour Paris Photo Match Crayon Concealer - Honey 3.2 gm
Electronics	INDIACASE Samsung Galaxy S9 Blue Translucent, Shockproof Back Cover
Fashion	Gatsby Analog Purple Dial With Silver Strap Watch For Women GTL135
Fashion	Sanwara Men Gold Art Silk Self Design Kurta and Pyjama Set
Electronics	Black Product
Electronics	Wiser Smart Homes Automation Gateway with App and Voice Control
Jewellery	Reliance Jewels Ag 99.9 2.9 gm Balaji Silver Idol
Jewellery	Reliance Jewels Bal Gopal Ovel Gold 24 KT 999 2 GM Coin
Fashion	Kiddiewink Cute Kid''s Soft Velvet Animal Cartoon School Backpack Bag for Baby Boy/Girl(2-6 Years) Pack of 2
Beauty	Fashion Colour Kiss Lip No Transfer Lipstick, 65 Purplish Red 2.6 gm
Fashion	I Jewels Traditional Gold Plated Kundan Pearl Payal Anklets Jewellery for Women & Girls (A034Q)
Fashion	LOF Round Metal Design Sunglasses For Women Wine Color Frame UV Protection Latest And Stylish (LS-D15139-C5I54I Brown Color Lens)
Beauty	Lakme True Wear Color Crush Nail Color Reds 31 9 Ml
Electronics	Black Product
Fashion	RC. ROYAL CLASS New Born Baby Pure Cotton Towel Terry Soft Socks (Pack of 5 Pairs)
Jewellery	Reliance Jewels 2 GM 24KT Gold Coin
Electronics	HANUMEX Han1038 Close Up Lense Filter For Nikon D3100 D5000 D5100 D3200 D3000 D40 D60 18-55mm AF-P Lens
Electronics	WETEK Matte 9H Hardness Guard for Lenovo Tab M10 FHD Plus 10.3" Inch
Beauty	Insight Cosmetics Concealer - Warm Yellow 3.5 gm
Fashion	Vatsalya Creation Alloy Necklace, Maang Tikka And A Pair Of Earrings For Women, Girls _ 9536Ramalct (Set Of 3)
Beauty	Divinectar Body Lotion - Extra Virgin Coconut Oil 400 ml
Beauty	Flormar Dewy Lip Glaze 04 Undressed 4.5 ml
Electronics	Beetel M90 Corded Landline Phone (Black)
Electronics	Belkin F2CU032BT06-BLK 1.8 m High Speed USB 2.0 to Reversible USB Type C Charge Cable, Black
Fashion	Camo Print Baseball Cap
Electronics	FOUR STAR FS-6166 VACUUM Corded and Cordless Trimmer for Men, Black
Beauty	AND EterlR & EtherlD EDP Pack of 2 100 ml
Fashion	Nakabh Antique Gold-Plated Crystal Blue Stone Studded Drop Earrings for Women Girls
Beauty	Flormar Dewy Lip Booster 02 Castle 4.5 ml
Jewellery	Reliance Jewels Bal Gopal Ovel Gold 24 KT 999 1 GM Coin
Beauty	Arata Natural Bath Essentials with Cleansing Shampoo & Body Wash for Intensive Nourishment 600 ml
Fashion	hangup Men Yellow Solid Poly Blend 3-Piece Sets
Beauty	Faces Canada Ultime Pro Hd Ace Base Radiance Primer 30 Ml
Electronics	Ambrane Multi-Purpose Trimmer (Aura S, Black)
Fashion	StoleVilla Women''s Printed Chiffon Multicolored Scarf and Stoles with Tassels - Set of 2
Electronics	JBL Tune 510 Bluetooth Wireless Stereo Headphone with Up to 40 hours of Battery Life, Multi-Point Connection, Rose
Fashion	CHiU Girls Black Casual Shoes
Electronics	Viblitz Black Camera Hand Grip Wrist Strap
Beauty	Eyetex Dazller Classique Compact Powder- 8008 Coffee 9 gm
Fashion	Swadesi Stuff Digital Green Dial Watch - ARMY GREEN (Boys)
Electronics	I Kall K21 Black Heart Rate Monitor Full Touch Smartwatch
Beauty	Blue Heaven Hypergel Nailpaint - Angel White, 101 11 ml
Electronics	Logitech M171 Wireless Mouse, Blue/Black
Fashion	Fashion Frill Trendy Double Coated Gold Plated Metal Chain
Jewellery	Reliance Jewels Laxmi Gold 24 KT 999 1 GM Coin
Electronics	Mi Dual Port 18 Watts QualComm Quick Charge 3.0 Dual USB Port BIS Certified Charger with Surge Protection
Beauty	Urban Gabru No Gas Hair Spray - Enrich with Aloe Vera & Jojoba Oil 100 ml
Electronics	Maharaja Whiteline Infiny Mix 150 Watts Hand Blender with Detachable SS Shaft
Beauty	L''Oreal Paris Revitalift Crystal Micro - Essence 130 ml
Electronics	Havells 28 litres Oven Toaster Grill (OTG), 28R BL with Motorized Rotisserie, 1500 W
Fashion	Men''s Height Increasing Elevator Formal Mocassin Slip-on Shoes
Beauty	VEGA X-Pro Professional Hair Clipper (VHCP-02) Black 1 gm
Electronics	Wearfit Edge HR and BP Monitor 1.69 Inch Pink Smart Watch For Unisex
Electronics	Apple iPhone 12 64 GB, White
Fashion	Casual Shoes For Women Waliking , Sneakers ,Loafers, Canvas casual shoes for Women Grey ORI(MM)-1679
Electronics	TRUEUPGRADE OnePlus 9 Pro Green Shock Proof Mobile Case Cover 10 x 8 x 7 cm
Fashion	FABIA Pink Women''s Casual Shoes
Electronics	Apple iPhone 12 256 GB, White
Fashion	Leaderachi Men Leather Brown Wallet With Key Ring And Pen (Haleatherswkp-Trifold-M)
Electronics	Wetek Black Silicone Mobile Phone Holder
Electronics	Hiffin Black 5 In 1 Lamp Bulb Holder
Electronics	Digitek Led Ring Light With Stand Drl-18Rc With No Shadow Apertures
Electronics	Western Digital 4 TB Portable Hard Disk Drive (HDD), WDBPKJ0040BBK Black
Electronics	realme 26.31 cm (10.4 inch) Wi-Fi Pad 3 GB RAM, 32 GB, Real Gold
Beauty	Physicians Formula The Healthy Powder SPF 16 - Tan - Warm DW2 7.5 gm
Electronics	Syska UltraTrim HT700 with 45 min Runtime, for Men, Black & Red
Fashion	HPS Sports Men Black Polycotton Solid Shorts (L)
Beauty	Arata Natural Mini Face & Oral Care Gift Box with Facewash(50 Ml), Face Serum Cream (50 Ml), Toothpaste (50 Ml) 150 ml
Fashion	BODYCARE Girls Multicolor Printed Cotton T-Shirt & Shorts Set
Fashion	Kids Girls/Baby Girls Cotton Printed Top and Pyjama/Nightwear Set (Pack of 1)
Fashion	CATCUB Girls Green All over print Single Jumpsuites
Jewellery	Reliance Jewels Laxmi Gold 24 KT (999) 10 GM Coin
Beauty	MADES Hair Care Wonder Volume Shampoo Luxurious Lifting 75 ml
Fashion	A.T.U.N. Girls Candy Creme Polka Full Sleeves Shirt Dress
Fashion	LUCKY JEWELLERY Bridal Wedding punjabi chuda Designer chura CZ Stone with Kundan Stone Maroon Color choora (891-G1C1-JM1436-M-210)
Beauty	Fashion Colour Kiss Lip No Transfer Lipstick, 03 Aubergine 2.6 gm
Beauty	Organic Harvest Vitamin-A Face Sheet Mask 20 gm
Fashion	GENTS SANDALS
Electronics	Zebronics BT7300RUCF Bluetooth Tower Speaker Supporting USB, SD, FM, AUX & Wireless Mic
Fashion	On Time Octus Analog Black Watch For Women (Pack Of 2)
Beauty	Ajmal 2 Wisal And 2 Nightingale Deodorants Pack of 4 200 ml
Beauty	Vega Eye Shadow Brush (PB - 06) 20 gm
Fashion	HPS Sports Men White Polycotton Solid Shorts (S)
Fashion	HPS Sports Men Dark Blue Polycotton Solid Shorts (S)
Beauty	Fashion Colour Lip Crayon, Waterproof, Long Lasting, 31 Pretty Please 2.8 gm
Beauty	Glimmer Nail Polish Geranium 5 ml
Electronics	Samsung Galaxy Tab S7 FE 31.50 cm (12.4 inch) Tablet 4 GB RAM, 64 GB, Mystic Pink, T735NA
Beauty	Maryaj Pebble Style EDP Spicy Woody Perfume And Maryaj Wild Stripes EDP Aromatic Oriental Perfume 200 ml
Jewellery	Reliance Jewels Ag 99.9 12.51 gm Ganesha Silver Idol
Electronics	LG 6.5 Kg Front Fully Automatic Washing Machine with 6 Motion Control Technology, FHM1065ZDL
Beauty	Myglamm Stay Defined Liquid Eyeliner Brow Powder - Walnut & Ebony 2.8 Gm
Beauty	Fashion Colour Terra Cotta Blusher, Shade 06 8 gm
Beauty	Ajmal Silver Shade EDP Citrus Woody Perfume And Kuro EDP Aromatic Spicy Perfume 190 ml
Beauty	Swati Cosmetics Coloured Lenses Turquoise 6 Month Contact Lenses ( - 4) 1''s
Beauty	nan
Fashion	Gansta Wayfarer Full-Frame Black Clear Sunglasses ,Men And Women ,Pack Of 3(GN3006-Blk-Brn-Clr-Com)
Electronics	WeCool Snug Fit Metallic C Type Earphones with Mic and Volume Controller
Electronics	iBELL DELUXEBK Tower Fan with 25 Feet Air Delivery, 4 Way Air Flow, High Speed, Anti Rust Body (Black)
Electronics	Sony SEL16F28 AE 16 mm Wide Angle Lens
Fashion	Luckza Multicolor Polyester Sport Bag 20 L
Electronics	Lee Star LE-802 2 Jars 400 W Mixer Grinder, Black
Beauty	Lotus Herbals Youthrx Active Anti Ageing Foaming Gel 50 Gm
Electronics	Niudart Black Tripod With Holder (Set Of 1)
Beauty	Ajmal Carbon Sacrifice II Him Deodorants (Pack of 2) 200 ml
Fashion	Rigo Men''s Maroon Black and Dark Grey Printed Cotton Sleeveless Vest T-Shirt-Pack of 2
Jewellery	Reliance Jewels Ag 99.9 20 gm Lakshmi Ganesh Silver Idol
Fashion	Lakme Fashion Purple Artificial Leather Shoulder Bag - 10 L
Electronics	JBL Quantum 100 Wired Gaming Headphone, Blue
Fashion	G1 Wonders Antiviral Antipollution face Mask
Fashion	Vighnaharta Gold Plated Alloy 7 Ring ,Women And Girls
Fashion	Zovim Blue Rubber Classic Boots - 5 UK
Fashion	Riara Women''s Satin Maxi Nighty Kaftan Kimono Sleeve Long Solid Nightdress Gown Sleepwear with Drawstring Pack of 3 (Corsair Blue & Jester Red & Terracotta)
Beauty	Color Fever Eye Bomb Metallic Eye Pencil cum Eye Shadow Water Proof - Quick Silver 1.8 gm
Jewellery	Reliance Jewels Ag 99.9 13.21 gm Lakshmi Ganesh Silver Idol
Electronics	Apple iPad Air 4th Gen 27.68 cm (10.9 inch) Wi-Fi Tablet, 256 GB, Sky Blue MYFY2HN/A
Fashion	AMACLASS Women''s Slippers Casual Flip Flop-Black
Fashion	Style Quotient Women Maroon Solid
Fashion	KVS Fab Women Brown Embroidered Net Semi-Stitched Lehenga Choli Set
Beauty	L''Oreal Paris Super Liner Superstar Duo Designer Eyeliner, Black 0.65 Gm
Electronics	HP 14a-na0003tu ChromeBook (Intel Celeron N4020/4GB/64GB eMMC/Intel UHD Graphics/Chrome OS/HD), 35.56 cm (14 inch)
Fashion	HPS Sports Men Green Lycra Blend Solid Shorts (XL)
Fashion	Fourfolds Boys Maroon Solid Cotton Blend Kurta Set
Beauty	Faces Canada Matte Nail Enamel Primrose Pink 47 9 Ml
Fashion	Riara Women''s Satin Silky Mini Solid Tunic Dress Mid Thigh Length Short Kaftan with Robe Night Suit Nighty Top (Terracotta, Free Size)
Fashion	Savage Men''s King Size Handkerchiefs For Men 100% Cotton White | Pack of 3 King Size Cotton Handkerchiefs for Men Daily Use | Business Handkerchief Size (45cms x 45cms) | Mens Clothing Accessories
Jewellery	Reliance Jewels Ag 99.9 14.94 gm Lakshmi Silver Idol
Fashion	Dreamrax Gold Plated Brass Bar Pendant Custom Name Necklace For W
Beauty	Nandika Beauty Facial Gel - Papaya 500 gm
Electronics	INDIACASE Galaxy A31,A51 Blue Shockproof,Anti-Scratch,Mirror Plating Stand Clear View Case Cover
Fashion	Cotton Rib Spaghetti with adjustable straps
Fashion	Footsoul Women''s Asta Flats (Grey) (FSL-459-7)
Electronics	Inclu For LG G3 Waterproof, Artificial Leather, Scratch Resident, Magnetic Lock Holster Case
Electronics	Apple iPad Pro 3rd Gen 2021 27.96 cm (11 inch) Wi-Fi + Cellular Tablet 16 GB RAM, 2 TB, Silver, MHWF3HN/A
Electronics	Wonderchef Egg Boiler With 7 Egg Poacher
Fashion	DIGIMART Boys Multicolored Designer Cotton Pack of 1 Kurta Pyjama Set
Beauty	SUGAR Cosmetics Arch Arrival Brow Powder - 04 Felix Onyx (Black for Black Hair) 1 gm
Fashion	HPS Sports Men Multicolor Polycotton Printed Tracksuit (XXL)
Jewellery	Reliance Jewels Ag 99.9 5.6 gm Ganesha Silver Idol
Jewellery	Reliance Jewels Ganesh Gold 24 KT (999) 5 GM Coin
Electronics	Hiffin Green 9Ft Stand Top Pipe Clips Curtains 6X10Ft E27 Double Holder Umbrella 20W Bulb Carry Bag (Set Of 1)
Electronics	TRUEUPGRADE Vivo V23 5G Lavender Shock Proof Mobile Case Cover 12 x 10 x 8 cm
Beauty	Swati Cosmetics Coloured Lenses Sapphire 6 Month Contact Lenses ( - 3.5) 1''s
Electronics	Olympus Camera E-M1M3 Mark III Interchangeable Lens Camera, Black
Electronics	BPL Head Shot MX 300 BWLH301 Bluetooth Headphone with 24 hours Playtime, Green
Beauty	Ajmal Titanium EDP Citrus Spicy Perfume And Carbon EDP Citrus Spicy Perfume 200 ml
Beauty	Ajmal Sacrifice For Her EDP Floral Musky Perfume And Blu EDP Aquatic Woody Perfume 140 ml
Beauty	Fashion Colour Cover Up Liquid Concealer, Shade 02 11 gm
Fashion	Prasub Silver Earrings Silver (Women, Girls)
Electronics	Apple Magsafe MC747HN/A 45 Watts Travel Adapter
Electronics	Xiaomi Redmi Note 10 Lite 64 GB, 4 GB RAM, Glacier White Mobile Phone
Jewellery	Reliance Jewels Ag 99.9 32.14 gm Lakshmi Ganesh Silver Idol
Fashion	Women Printed Cotton Lower | Women Printed Cotton Track Pant | Women Printed Cotton Active Wear | Women Printed Cotton Pyjama
Beauty	Nature''s Essence Protecting Face Wash Gel - Neem & Aloe 65 ml
Beauty	Swati Cosmetics Coloured Lenses Pearl 6 Month Contact Lenses ( - 2.5) 1''s
Jewellery	Reliance Jewels 1 GM 24KT Gold Coin
Beauty	Plantas Skin Firming Organic Face Scrub 50 ml
Fashion	Royal Son Cat Eye Polarized Women Sunglasses
Jewellery	Reliance Jewels Shree Round Gold 24 KT 999 1 GM Coin
Beauty	Daily Life Forever52 Glitz Waterproof Eyeliner Eyeshadow Glt010 0.6 gm
Electronics	Inclu For LG k9 Waterproof, Artificial Leather, Scratch Resident, Magnetic Lock Holster Case
Jewellery	Reliance Jewels Mahavir Ji Round Gold 24 KT (999) 4 GM Coin
Electronics	Viblitz Black Photography Tripod With Carry Bag (Pack of 2)
Electronics	WIB Grey Blood CIrculation Machine Massager
Fashion	Tace Women Multicolor Solid Cotton Blend Pack of 2 Lingerie Sets
Beauty	Zayn & Myza Breathable Nail Enamel With Raspberry & Almond Oil, Rose Macaroon 6 ml
Fashion	Trysco Girls Genuine Leather Tan Belt
Electronics	Strombucks Black Tripod, Mobile Flash (Pack Of 2)
Beauty	Ajmal 2 Silver Shade And 2 Distraction Deodorants Pack of 4 200 ml
Fashion	Sanwara Men Beige Art Silk Self Design Kurta and Pyjama Set
Jewellery	Reliance Jewels Ag 99.9 7.76 gm Ganesha Silver Idol
Jewellery	Reliance Jewels Ag 99.9 18.88 gm Ganesha Silver Idol
Jewellery	Reliance Jewels OM Round Gold 24 KT 999 1 GM Coin
Fashion	Bersache Men Casual Sandal (Black)
Beauty	Ajmal 3 Blu Deo & Aretha EDP Pack of 4 20 ml
Electronics	DAMDAM Smartwatch Screen Guard Boat Xtend 1.69 (Pack of 2)
Fashion	BownBee Girls Orange Printed Cotton Lehenga Choli Set
Fashion	SIDEWOK Combo of 3 Polka Dot Print Casual Sleek Belt For Women/Girls (Combo-3)
Beauty	AND MystE EDP & DaintyG Mist Pack of 2 250 ml
Fashion	Calfnero Women Black Genuine Leather Wallet
Jewellery	Reliance Jewels Ag 99.9 4.58 gm Ganesha Silver Idol
Electronics	MVTECH Fibre Screen Protector for Samsung Galaxy Tab A7 Lite 8.7inch
Fashion	Leaderachi Men Leather Green Wallet And Belt Combo (Rakhi-Wb-23Gr)
Jewellery	Reliance Jewels Silver 999 5 GM Coin
Electronics	Fitup Black Gorilla Tripod With Holder (Set Of 1)
Beauty	Revolution Skincare 0.5% Retinol Super Serum with Rosehip Seed Oil 30 ml
Beauty	Flormar Nail Enamel 228 Bordeaux Red 11 ml
Fashion	Cotton Shirt with Patch Pocket
Beauty	Ajmal Aurum Raindrops Sacredlove Deodorant Spray (Pack of 3) 200 ml
Beauty	Ajmal Asher Concentrated Perfume Oil Oriental Attar And Majmua Concentrated Perfume Oil Oriental Attar 22 ml
Electronics	BlueRigger Cat 6 Ethernet Cable - 4.5 m
Beauty	Maryaj Edp Tuxedo For Him 100 Ml
Electronics	MVTECH USB 2.0 Male to Male Data Cable 0.50 Meters for Computer PC Hard Disk Video Capture Black
Jewellery	Reliance Jewels 10 GM 999 Silver Coin
Beauty	Allure Blush Brush (blush Brush C-28) 1''s
Fashion	Underjeans by Spykar Blue Cotton Boxer Shorts For Mens
Fashion	Abaranji Men White Pink Solid Pure Cotton Dhoti (Free)
Beauty	Lash Illusion Mascara Dm001 4 Ml
Fashion	KFN5391
Fashion	Time Up Digital White Watches For Boys And Girls (Pack Of 2)
Beauty	NOTE LUMINOUS SILK MONO EYESHADOW 18 4.5 gm
Beauty	L.A. Colors Mega Dramatilash Mascara Black 13 ml
Electronics	Vacuum Cups Chinese Medicine Magnet Therapy Cupping Set Acupuncture Massager /Kangzhu Vaccum Cupping Therapy Set (24 Cups)
Jewellery	Reliance Jewels Laxmi Silver (999) 5 GM Coin
Jewellery	Reliance Jewels Swastik Round Gold 24 KT 999 1 GM Coin
Electronics	Reconnect Mickey Sandwich Maker with Theme Impression, Non-Stick Plates, Cool Coating for Burn-Free Touch, Heat-up Light Indicator, Lid Lock, Compact Vertical Storage, 2 Years Warranty
Fashion	MIS1011_10
Fashion	PD-502-DGREY_7
Electronics	Gizmore GIZ MN221 Ultra Beat Bluetooth Wireless Earphone with Dual Pairing & Fast Charging (Green)
Beauty	Ajmal Aura Concentrated Perfume Oil Floral Fruity Attar And Mukhallat Raaqi Concentrated Perfume Oil Floral Fruity Attar 20 ml
Beauty	Soulflower Pure Tea Tree Soap 150 gm
Electronics	Brayden Rizo 700 W Electric Rice Cooker with One-Step Automatic Cooking (Crimson Red, 1.8 Litre)
Electronics	Belkin F8J207BT04-GLD MFi Certified Kevlar USB to Lightning Cable, Gold
Beauty	Faces Canada Ultime Pro Blendfinity Stick Ivory 01 10 Gm
Electronics	SellZone Laptop Battery Compatible For Hp Pavilion 15-N270Tx(SZG0H1014)
Fashion	Pack of 2 Printed Round-Neck T-shirts
Fashion	G1 Wonders Antiviral Antipollution face Mask
Fashion	Popster Red Printed Cotton Round Neck Regular Fit Half Sleeve Womens T-Shirt
Electronics	Bosch TrueMixx Joy 500 Watts Mixer Grinder with 3 Jars, Red
Fashion	Banjoy High Ankle Boots For Women
Fashion	Creature Sports Men''s Ankle Length Socks Pack of 3(SCS-701)
Electronics	WIB Trimmer , 15 cm x 8 cm
Beauty	Myglamm Lit - Ph Lip Balm - Bite Me 2 Gm
Fashion	Royal Son Narrow Rectangular UV Protection Women Sunglasses
Fashion	hangup Men Parrot Solid Blend 2-Piece Sets
Fashion	Acnos Analog Pink Dial Silver Strap Watch For Women - (JL-PINK)
Beauty	DeBelle Gel Nail Lacquer Blueberry Crepe Lavender Nail Polish 8 ml
Beauty	Lafz Transfer Proof & Smudge Proof Velvet Matte Lip Colour, Spice Ginger 5.5 ml
Electronics	WIB Black Automatic Hair Curler
Electronics	Ali Creation Silicon Strap Accessory For Xiaomi Mi Band 5 (Green)
Fashion	HPS Sports Men Maroon Lycra Blend Solid Shorts (S)
Electronics	Zoshomi 400W Room Heater with Digital Display
Jewellery	Reliance Jewels Ag 99.9 3.24 gm Ganesha Silver Idol
Beauty	Revolution Skincare EGF Serum 30 ml
Electronics	Zapcase Black Rubber Back Cover For Samsung Galaxy F41 19.5 x 13.5 x 2 cm
Fashion	FIMS - Fashion is my style Women Black Solid Cotton Blend Pack of 3 Bra Hook Extender 2 Hook 3 Eye
Fashion	Louis Devin Smart Analog Multicolor Watch For Women (Ld-L105-Blu-Ch)
Fashion	Cotton Rib Spaghetti with adjustable straps
Fashion	Unisex Eyewear
Beauty	Gemblue Biocare Rose Petal Mask 500 ml
Fashion	P200V4_CO2_32_4
Fashion	On Time Octus Analog Multcolor Watch For Women (Pack Of 2)
Fashion	SIDEWOK Men Ankle/Half socks Pack of 5 Pairs (SCS-HL-06)
Beauty	Vaadi Herbals Anti-Acne Face Pack - Neem 120 gm
Fashion	HPS Sports Men Red Polyester Solid Jacket (XXL)
Electronics	Hindware Bianco Caeli 3 Blade 1200 mm Ceiling Fan Silent Operation, White
Electronics	Inalsa 30 litres Oven Toaster Grill (OTG), Masterchef 30 SSRC
Beauty	Fashion Colour Kiss Lip Balm, Shade 02 3.6 gm
Electronics	Geek Aire GF3 4 Blade 5 inch Rechargeable Handheld Fan with 2500 mAh Li-ion Battery, Pink
Fashion	HANGUP Men Blazer Polyester Viscose Regular Fit Solid BlueTuxedo2_Blazer
Electronics	TP-Link TL-MR6400 V3 300 Mbps Wireless N 4G LTE Router black
Fashion	Heaven Decor Superman & Minnie Soft Velvet Kids School Bag Nursury Class To 5 ( Size - 14 inch )
Fashion	LORENZ Combo of Blue Watch & Wallet for Men | CM-1093WL-06
Fashion	CALYPTO Analog Rose Gold Dial Rose Gold Strap Watch For Women ST-293
Electronics	Kent Gem 16058 Induction Cooktop with LED Display and Simple Controls and 5 Pre-Set Function
Electronics	Fossil Q Gen 4 Hr FTW6015 Smart Watch, Nude
Beauty	Beauty People Matte Lucious Liquid Lip Colornude - In - Pink - L30 
Beauty	AND EterlR & EtherlD EDP Pack of 2 150 ml
Electronics	Nokia G20 64 GB, 4 GB RAM, Glacier Mobile Phone
Fashion	Sanwara Men Maroon Pure Silk Self Design Kurta and Churidar Set
Beauty	Ajmal Bastion EDP Woody Aromatic Perfume And Oudh Mukhallat Concentrated Perfume Oil Oriental Oudhy 106 ml
Jewellery	Reliance Jewels Ag 99.9 2.31 gm Ganesha Silver Idol
Beauty	Bella Vita Organic Strawberry 3 In 1 Tinty For Lips 8 gm
Electronics	Philips HU4706 14 Watt Air Humidifier with NanoCloud humidification technology, White
Beauty	Fashion Colour Vivid Matte Lipstick, 23 Chestnut 3.8 gm
Beauty	Ajmal Impress Concentrated Perfume Oil Citrus And Maryaj Direction East EDP Citrus Spicy Perfume 110 ml
Electronics	BlueRigger Cat 6 Ethernet Cable - 30 m
Beauty	mCaffeine Exfoliation & Tan Removal Combo 200 gm
Fashion	Kiddiewink Cute Kid''s Soft Velvet School Backpack Bag for Kids (2 to 6 Years)
Fashion	Shirt with Pants & Suspenders Set
Fashion	Kid''s fancy denim and cotton dungaree suits
Fashion	Kleat Men''s Blue Synthetic leather Party Formal Shoes
Beauty	Allure Concealer Brush - (142s) 1''s
Jewellery	Reliance Jewels Swastik Round Gold 24 KT 999 2 GM Coin
Electronics	Inbase Urban Lite Z Smart Watch with Multiple Sports mode, IPX68 Waterproof Resistance, Black
Electronics	Apple iPad Air 5th Gen 2022 27.69 cm (10.9 inch) Wi-Fi + Cellular Tablet, 256 GB, MM743HN/A, Starlight
Electronics	Riviera Mobile Battery For Karbonn K44
Beauty	INSIGHT COSMETICS DIP AND GO NAIL POLISH REMOVER - GREEN APPLE 20 ml
Beauty	Fashion Colour Face Highlighter Bronzer And Illumintor, Shade 04 7.5 gm
Fashion	Vast Unisex Adult & Unisex Child Rectangular Sunglasses
Electronics	OpenTech Tempered Glass Screen Protector For Oneplus 6T
Beauty	Ajmal Aurum And Aurum Deo & Prose EDP Pack of 3 20 ml
Beauty	Bonjour Paris Coat Me Satin Matte Nail Polish - Blue Mood 9 ml
Fashion	BownBee Girls Orange Woven Velvet Lehenga Choli Set
Beauty	Medimade Vitamin E Body Butter (Pack of 2) 1''s
Fashion	AHIKA Women Dark Green Pure Cotton Printed Kurta and Pant Set (L)
Beauty	Miss Claire Glimmersticks For Eyes E-02 Silky Grey 1.8 Gm
Electronics	Black Product
Fashion	Pearl Night Wears Womens Black Cotton Shirt And Pyjama Set - Medium
Electronics	Torlen Professional TOR CC 01 Silver Hair Curling Iron - Set of 3"
Fashion	Kid''s fancy denim and cotton dungaree suits
Beauty	Ajmal Carbon EDP Citrus Spicy Perfume And Viola EDP Fruity Floral Perfume 175 ml
Beauty	Uncle Tony Face Scrub 200 ml
Beauty	Fashion Colour 24hr Longwear Liquid Foundation With Skin Care, Sunsrise 30 ml
Electronics	Bose SoundLink Revolve Plus II BT Multimedia Speaker with Up to 17 hours Battery, Triple Black
Electronics	Lee Star LE-801 250 W Chopper, Black
Fashion	Aawari Women Dark Blue Dyed Lycra Blend Single Trousers (XL)
Fashion	Brauch Neon Green Sneakers For Women
Beauty	Elinor Vitamin C Face Wash + Vitamin C with Hyaluronic Acid Face Serum + Vitamin C Spf 20 with Hyaluronic Acid & Rosehip Oil Cream 180 gm
Beauty	Ajmal Senora EDP Floral Spicy Perfume And Mukhallat Raaqi Concentrated Perfume Oil Floral Fruity 85 ml
Beauty	VEGA Classic Hair Crimper with Ceramic Coated Plates (VHCR-01) Black 1 gm
Beauty	Arata Natural Damage Repair Duo With Hydrating Shampoo(75 Ml) & Conditioner(75 Ml) Daily Damage Repair 150 ml
Jewellery	Reliance Jewels Ag 99.9 8.95 gm Saraswati Silver Idol
Fashion	Jewels Galaxy Stylish Pearl Gold Plated Hairclips for Women/Girls
Fashion	Moon Walk Black Fashionable Flats for Women
Electronics	Zeekart Black Smart Watch With Heart Rate Monitor For Men And Women
Fashion	Trysco Women Genuine Leather Red Belt
Electronics	Inalsa 1.8 litres 1500 Watts Electric Kettle, Wow
Fashion	Sanwara Men White Art Silk Solid Kurta and Pyjama Set
Beauty	O-Lens Jenith 6Month Coloured Contact Lenses - Brown ( 0.00 ) 1''s
Beauty	Archies Parfum NEW BOYZ PARFUM ORIGINAL 50 ml
Beauty	I AM EYECONIC 3D GLITTER FIREBALL 4 gm
Beauty	Maryaj Tuxedo EDP Spicy Woody Perfume And Maryaj Dynamic EDP Spicy Woody Perfume 200 ml
Electronics	INDIACASE Vivo V11 Pro Green Shockproof, Slim Fit, Drop Protection Back Cover
Beauty	Wet N Wild Eye Brow Pomade Medium Brown 2.5 gm
Jewellery	Reliance Jewels Ganesh Gold 24 KT (999) 10 GM Coin
Beauty	Vigini V-Tightening & Whitening Gel 100 gm
Electronics	Kushi Screen Guard for Samsung Galaxy A5
Beauty	Insight Cosmetics HD Conceal - Pista Green 8 gm
Electronics	Nillkin Tempered Glass for Apple iPhone 13 Pro Max
Jewellery	Reliance Jewels Ag 99.9 10.93 gm Bal Krishna Silver Idol
Fashion	Kiddiewink Cute Kid''s Soft Velvet Animal Cartoon School Backpack Bag for Baby Boy/Girl(2-6 Years) Pack of 2
Electronics	MVTECH Mini HDMI Male to HDMI Female Adapter Converter Plug (Pack of 2) Standard HDMI Device Using a Standard HDMI Cable.(Black)
Fashion	Swadesi Stuff Digital Blue Dial Sports Watch - JUICE SKYBLUE (Boys & Girls)
Fashion	HPS Sports Men Blue Polycotton Solid Shorts (XL)
Beauty	House of Aroma Passion Fruit Fragrance Oil 10 ml
Electronics	Garmin vívosmart 4 Smart Watch, Gray
Electronics	Black Product
Beauty	Medimade Hair Repair Shampoo With Linden Bud Extracts 300 ml
Beauty	Swati Cosmetics Aquamarine Coloured Lenses 6 Month Contact Lenses 1''s
Electronics	LG 7 Kg Semi-Automatic Top Load Washing Machine with Rat Repellent Chemical., P7010RRAA, Burgundy
Electronics	Groomiist Platinum Series Corded/Cordless 3 in 1 Grooming Kit PST-501 with Floating Charging Indicator & Charging Stand: 90 Minutes Running Time & 700mAh Lithium-Ion Battery (Black)
Fashion	Underjeans by Spykar White Cotton Brief For Mens
Beauty	Ajmal Nightingale And Persuade For Men & Women And Sacrifice II For Him Deodorants Pack of 3 200 ml
Beauty	Ajmal Blu EDP Aquatic Woody Perfume And Raindrops EDP Floral Chypre Perfume 140 ml
Electronics	Inalsa Vapor Max Garment Steamer
Beauty	Fashion Colour Hair Serum 100 ml
Fashion	Sanwara Men Maroon Dupion Silk Self Design Kurta and Churidar Set
Electronics	Samsung 60.96 cm (24 Inch) QHD Computer Monitor with IPS Panel, LS24A600NWWXXL , Black
Beauty	COAL Clean Beauty , Honey and Saffron Soap 100 ml
Electronics	JBL Partybox Encore Essential Portable Party Speaker with 100W Sound
Beauty	Swati Cosmetics Coloured Lenses Pearl 6 Month Contact Lenses ( - 3) 1''s
Fashion	AD & AV Boys Multicolor Solid Denim Single Jeans
Electronics	Samsung 1 Ton 5 Star AR12BY5YATA Inverter Split AC, HD Filter, 2 Way Swing, Floral Design, 5 in 1 Convertible (2022 Launch)
Beauty	Blue Heaven Hypergel Nailpaint - Velvet Wine, 508 11 ml
Jewellery	Reliance Jewels Bal Gopal Round Gold 24 KT 999 2 GM Coin
Beauty	Daily Life Forever52 Eye Shadow Brush Nx018 1''s
Beauty	mCaffeine Coffee Lip Sleeping Mask 12 gm
Beauty	Bio Bhringraj Oil 100 Ml
Beauty	Miss Claire Glitter Palette 15 Gm
Jewellery	Reliance Jewels RL Gold 24 KT (999) 10 GM Coin
Fashion	Wildhorn Men Grey Laptop Bag
Fashion	Typographic Print Crew-Neck T-shirt
Beauty	Ajmal Desert Rose EDP Floral Oriental Perfume And Sacrifice II For Him Deodorant Fruity Aromatic Fragrance 300 ml
Beauty	The Face Shop Rice Water Bright Foaming Cleanser 150 Ml
Fashion	Buy That Trendz Women Multicolor Solid Cotton Viscose Lycra Patiala Pants (Pack of 3)
Electronics	Wengvo Black Ring Light With Tripod (Set Of 1)
Beauty	Beauty People Natural HD Matte Lip Crayon Vivid - 102 4 gm
Electronics	LG XBOOM OK75 1000 watts Party Speaker with Karaoke
Electronics	Rozia Gold Hair Curler
Beauty	Ajmal Silver Shade EDP Citrus Woody Perfume And Asher Concentrated Perfume Oil Oriental 112 ml
Beauty	Maryaj Deuce Femme EDP Floral Fruity Perfume And Ajmal Wisal Deodorant Floral Musky Fragrance 300 ml
Fashion	Moon walk Brown Fashionable Bellies for Women
Jewellery	Reliance Jewels Flower Round Gold 24 KT (999) 4 GM Coin
Beauty	Rejuvenating UBTAN Lip Balm - Rose 5 gm
Beauty	Organic Harvest Coffee Conditioner 500 ml
Electronics	Kenstar Senator SS 500 Watts Mixer with Power Plus Hybrid Motor, White (KMSEN50W3S-DES)
Beauty	Neemli Naturals Argan & Rose Day Cream 50 ml
Beauty	Ajmal Shine EDP Floral Powdery Perfume And Oudh Mukhallat Concentrated Perfume Oil Oriental Oudhy 81 ml
Beauty	Garnier Skin Naturals Bright Complete Vitamin C UV Serum Cream 45 gm
Beauty	Daily Life Forever52 Eye Brow Brush Nx025 1''s
Fashion	Sanwara Men Black Pure Silk Self Design Kurta and Churidar Set
Beauty	Be Soulfull Off To A Great Start Facial Cleanser 100 ml
Electronics	NAMIBIND 14 Sheets Cross Cut Paper Shredder Machine - Multicolor
Fashion	GSA MALLWomen Blue Solid Denim Jacket
Fashion	Kleat Men''s White Synthetic leather Formal Shoes
Electronics	Intex IT-WLKBM01 POWER Wireless Keyboard & Mouse Combo Set(Black)
Electronics	Samsung 1.5 Ton 4 Star AR18BY4YATA Inverter Split AC,HD Filter, 2 Way Swing, Floral Design, 5 in 1 Convertible (2022 Launch)
Electronics	Scratchgard Anti-Glare Screen Guard for iBall Slide 3G Tab 6095-Q700
Electronics	Black Product
Electronics	WIB Combo pack of Aloe Vera Gel Face Mask and Body Massager (Pack of 7)
Fashion	Shiv Textiles Women Pink Digital Print Crepe Kurti
Beauty	Bonjour Paris Coat Me Neon Satin Matte Nail Polish - Fluorescent Red 9 ml
Fashion	Underjeans by Spykar Blue Cotton Trunk For Mens - Pack of 2
Beauty	Organic Harvest Anti Dandruff Shampoo (ACV) 500 ml
Jewellery	Reliance Jewels Ag 99.9 7.33 gm Lakshmi Ganesh Silver Idol
Beauty	Chambor Gel Effectnail Lacquer Mellow Mood - 0315 30 ml
Fashion	SPLAZOS Latest Design Green Round Dial Genuine Leather Strap Analog Watch For Girls And Women
Jewellery	Reliance Jewels 5 GM 999 Silver Coin
Beauty	Swati Cosmetics Coloured Lenses Turquoise 6 Month Contact Lenses ( - 4.75) 1''s
Jewellery	Reliance Jewels Bal Gopal Round Gold 24 KT 999 1 GM Coin
Beauty	Glimmer Premium Nail Enamel Navy Blue 10 ml
Fashion	In Care Lingerie Women White Hosiery Bra
Fashion	Tooba Handicraft Red Velvet Girls Designer Clutch Bag With Shoulder Strap
Beauty	Ajmal Senora EDP Floral Perfume & Maryaj Goldie EDP & M For Her EDP 1''s
Jewellery	Reliance Jewels Ag 99.9 7.82 gm Ganesha Silver Idol
Electronics	Nirlep Selec+ Non Stick Induction Flat Tawa, IJFT27N, 5 mm
Beauty	Vega Graduated Dressing Comb (HMBC - 122) 32 gm
Electronics	Kelvinator 584 litres Side By Side Refrigerator, Black KRS-A600BKG
Electronics	Fitup Black Tripod
Fashion	DIAZ Boys Printed Pure Cotton Track Pants (Pack of 3)
Fashion	Underjeans by Spykar Grey Cotton Boxer Shorts For Mens
Beauty	Bonjour Paris Satin Matte Nail Polish - Red 9 ml
Electronics	Samsung Galaxy S21 FE 5G 256 GB, 8 GB, Olive, Mobile Phone
Beauty	Precision Eye Liner Eye Liner Liquid Eln001 2.5 Ml
Electronics	Samsung Galaxy Active 2 SM-R820NZKA Smart Watch with Stress Tracker and Wireless Magnetic Charger, Black
Electronics	LG 7 Kg Top Fully Automatic Washing Machine with Smart Inverter Technology, T70SNSF3Z
Electronics	Athots Blue And White Foster Pro Powerful Mixer Grinder With 4 Jars 550 W
Beauty	Glimmer Nail Polish Red Love 5 ml
Electronics	Nillkin Tempered Glass for Apple iPhone 7 Plus
Beauty	Bella Voste Luxe Matt Chrome Shade 222 10 Ml
Jewellery	Reliance Jewels Mahavir Ji Round Gold 24 KT 999 1 GM Coin
Electronics	Amazon Echo Show 5 (2nd Gen) Smart Multimedia Speaker with Built-in Camera, Black
Beauty	Teal & Terra Hairfall And Dandruff Treatment Oil 100 ml
Electronics	Samsung T70 2.0 Channel 1500 Watts Party Speaker
Fashion	PV 01
Beauty	Lenphor Nail Tint Clear Snow 50 12 Ml
Beauty	Ajmal Diza EDP Fruity Floral Perfume And Aurum EDP Fruity Floral Perfume 175 ml
Beauty	Medimade Anti Dandruff Shampoo With Tea Tree & Ginger Oil 300 ml
Beauty	Blue Heaven Hypergel Nailpaint - Romantic Rose, 503 11 ml
Fashion	Mikado Analog Multicolor Watch For Girls
Fashion	Memoir Silver Plated Stainless Steel Pendant Black and Silver (Men and Women)
Electronics	Beetel X73 Cordless 2.4Ghz Landline Phone with Caller ID Display, 2-Way Speaker Phone with Volume Controls, Auto Answer, Alarm, Stylish Design (Black)
Fashion	SS22_SOHEAR1345
Electronics	Artway Fur Wallpaper Laptop Skin For 17 inch Laptop
Electronics	Zapcase Black Rubber Back Cover For Xiaomi Redmi Note 10 19.5 x 13.5 x 2 cm
Electronics	Ali Creation Screen Protector For Mi Band 2 (Pack Of 2) (Transparent)
Fashion	IndiWeaves Girls Cotton Printed Skirts (Pack of 4)
Electronics	Milagrow SilverFox 21 Dry & Wet Robotic Vacuum Cleaner, Remote Control, 600ml Large Dust Bin & 110ml Water Tank, 1500Pa Suction Power, 4 Cleaning Modes, Self-Charging
Beauty	Miss Rose 18 Color Matte & Glitter Highly Pigmented Eyeshadow Palette 7001 - 001B 21 gm
Electronics	Mobi Elite Multicolor Plastic Back Cover For Mi Redmi Y2
Electronics	Gionee Gbuddy SYMPHONY 105 Wireless Earphone with Dual Pairing, Voice Assistant (Silver)
Beauty	Revlon Top Speed Hair Color Woman-Natural Brown 60 40 Gm
Beauty	Revlon Colorstay Gel Envy Long Wear Nail Enamel - Diamond Top Coat 11.6 Ml
Beauty	Ajmal Viola EDP Fruity Floral Perfume And Aurum EDP Fruity Floral Perfume 150 ml
Electronics	TRUEUPGRADE Vivo iQOO Z5 5G Purple Shock Proof Mobile Case Cover 10 x 8 x 7 cm
Fashion	Savage Girls Cotton Bloomers for 9 to 10 years old 70cm Pack of 6 Assorted Colors
Fashion	Floral Print Straight Kurta
Fashion	Epic Toys DWATCH-BLACK Black Silicone Digital Watch For Unisex Child
Fashion	Cherry Crumble by Nitt Hyman Unisex Multicolor Colorblock Cotton Shirt
Fashion	Heaven Decor Mickey Velvet Soft Plus kids School Bag Nursury class to 5 ( Size - 14 inch )
Beauty	Vega Wide Tooth Wooden Comb (HMWC - 05) 25 gm
Electronics	Inalsa Bullet Mini Chopper
Beauty	LA French AMBITION Perfume for Women 100 ml
Beauty	Bio Morning Nectar Flawless Lightening Eye Cream Spf- 30Uva/Uvb 15 Gm
Fashion	Underjeans by Spykar Red Cotton Trunk For Mens - Pack of 2
Electronics	Viblitz Red and Black Card And Battery Box
Electronics	Reconnect 5200 mAh Power Bank, PT5200-RF
Electronics	Ambrane 10000 mAh Lithium Polymer Powerbank, PP-115, White
Electronics	Clearline 200W Food Warming Tray, Silver FWT01
Beauty	Ajmal Aurum Avid Silvershade Deodorant Spray (Pack of 3) 200 ml
Beauty	Ajmal Mukhallat AL Wafa Concentrated Perfume Oil Oriental Musky Attar And Mizyaan Concentrated Perfume Oil Oriental Musky Attar 26 ml
Fashion	Vast TRU BLU Cat Eye Blue Ray Blocking Anti Glare UV Protection Full Frame Spectacles Eyeglasses For Mobile, Laptop, Tablet, Computer Zero Power
Electronics	Stuffcool Flow WCFLOW25 Dual USB Port Tarvel Charger
Beauty	Swati Cosmetics Coloured Lenses Honey 6 Month Contact Lenses ( - 3) 1''s
Fashion	Vatsalya Creation Alloy Necklace With Pair Of Earrings For Girls _ 532 Rama (Set Of 2)
Beauty	Glimmer Ne Chrome Pink 5Ml Btl M 18 ml
Electronics	Reconnect RAHCB1001 2 m supports 1080p, 3D Compatible, 4K Cinema HDMI Cable, Black
Electronics	Lifelong LLM27 Electric Handheld Full Body Massager
Fashion	Women Shoulder Handbag - Combo of Two - Khaki & Purple (H004KK_H006PL)
Fashion	MarkQues Men''s Watch and Leather Belt Combo Gift Set for Men (IND-770101-NL-1102)
Electronics	Inclu For Moto G7 POWER Waterproof,Artificial Leather,Anti-Scratch,Magnetic Lock Holster Case
Electronics	Mivi Turquoise Play Bluetooth Speaker With 12 Hours Playtime Built In Mic
Beauty	Ajmal Mercurial Thunder Edt Pack of 2 500 ml
Beauty	Fashion Colour Pro Hd Contour & Highlighter Palette, Shade 03 12 gm
Electronics	Black Product
Fashion	DIAZ Women Printed Pure Cotton Track Pants (Pack of 2)
Beauty	Freeskin Charcoal Shower Gel 400 ml
Fashion	Mikado Analog Blue Watch For Girls
Electronics	TP-Link Deco M5 AC1300 Whole Home Mesh Wi-Fi System White
Fashion	RC. ROYAL CLASS Men''s Calf Length Cotton Formal Multicolored Socks (Pack of 5 Pairs)
Electronics	Reconnect BC06202 8 x 25 Binocular
Beauty	mCaffeine Naked & Raw Latte Coffee Bathing Bar Soap for Moisturization with Almond Milk 100 gm
Fashion	Joven Men Checked Boxer Pack Of 3 Shorts
Beauty	Ajmal Distraction And Magnetize For Men & Women And Aurum Femme Deodorants Pack of 3 200 ml
Jewellery	Reliance Jewels Ag 99.9 3.09 gm Lakshmi Silver Idol
Beauty	Reequil Pore Refining Niacinamide Serum 25 ml
Fashion	Elite Crafts Stylish PU Leather Adjustable Automatic Buckle Sliding Belt For Men, Blue
Electronics	INDIACASE Samsung Galaxy S10 Lite Black Translucent, Shockproof, Hard Back Cover
Fashion	BODYCARE Girls Blue Printed Fleece Top & Pyjamas Set
Beauty	Ajmal Aristocrat EDP Citrus Woody Perfume And Khofooq Concentrated Perfume Oil Woody Oudhy 93 ml
Electronics	Rodak Vacuum Cartridge Filter, Yellow
Electronics	Infinity (JBL) Clubz 250 Dual EQ Deep Bass 15W Portable Waterproof Wireless Speaker Blue
Electronics	Samsung Galaxy A73 5G 128 GB, 8 GB RAM, Awesome White, Mobile Phone
Jewellery	Reliance Jewels Ag 99.9 13.57 gm Ganesha Silver Idol
Jewellery	Reliance Jewels Ag 99.9 17.28 gm Shiva Silver Idol
Beauty	Mothercare Quick Absorb Diaper Pants (XL) 40''s
Beauty	Vega Shampoo Comb (HMC - 30) 57 gm
Fashion	Memoir Gold Plated Brass Goldplated thick and Heavy Chain Men and Women
Electronics	Apple iPhone 13 Pro 512 GB, Graphite
Fashion	Hangup Men Blazer Polyster Viscose Regular Fit Printed D135_5Button_Blazer
Fashion	hangup Men Orange Solid Polyester Blend Kurta Pyjama Set
Beauty	Ajmal Primitive Forests Edt Of 2 & Distraction Deodorant Pack of 2 450 ml
Fashion	Luv Byt Trendy White Heels For Women
Fashion	Underjeans by Spykar White Cotton Boxer Shorts For Mens - Pack of 2
Beauty	Medimade Olive Body Butter 200 ml
Jewellery	Reliance Jewels Ag 99.9 3.09 gm Ganesha Silver Idol
Beauty	Ajmal 2 Persuade & Magnetize Deo & Prose EDP Pack of 3 20 ml
Fashion	Printed A-line Dress with Tassels
Jewellery	Reliance Jewels Laxmi-Ganesh Silver (999) 5 GM Coin
\.


--
-- Data for Name: left_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.left_table (aggregate) FROM stdin;
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
title (deluxe)\nmeghan trainor\n 2014, 2015 epic records, a division of sony music entertainment\n9-Jan-15\ncredit\n2:51
slow down (remixes)\nselena gomez\n 2013 hollywood records, inc.\n20-Aug-13\nslow down (smash mode remix)\n5:21
slow down (reggae remixes) - single\nselena gomez\n 2013 hollywood records, inc.\n20-Aug-13\nslow down (sure shot rockers reggae dub remix)\n3:15
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
the reason - ep\nx ambassadors\n 2015 kidinakorner/interscope records\n10-Aug-15\nshining\n3:40
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25
hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28
hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28
hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28
hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28
hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand© & professor green)\n4:15
get free - single\nmajor lazer\n 2013 secretly canadian / mad decent\n27-Feb-13\nget free (andy c remix)\n5:31
original don (feat. the partysquad) [remixes] - ep\nmajor lazer\n 2011 downtown records unders exclusive license to interscope records in the u.s.a.\n1-Nov-11\noriginal don (feat. the partysquad) [the partysquad & punish smash em remix]\n3:38
peace is the mission\nmajor lazer\n 2015 mad decent\n1-Jun-15\nall my love (feat. ariana grande & machel montano) [remix]\n3:49
original don (feat. the partysquad) [remixes] - ep\nmajor lazer\n 2011 downtown records unders exclusive license to interscope records in the u.s.a.\n1-Nov-11\noriginal don (feat. the partysquad) [the partysquad & punish smash em remix]\n3:38
get free - single\nmajor lazer\n 2013 secretly canadian / mad decent\n27-Feb-13\nget free (andy c remix)\n5:31
nick jonas (deluxe version)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48
nick jonas\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\nnothing would be better\n4:34
nick jonas (deluxe)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48
nick jonas (deluxe)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48
nick jonas\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\nnothing would be better\n4:34
#NAME?\ned sheeran\n 2011 warner music uk limited\n9-Sep-11\nsunburn\n4:35
5\ned sheeran\n 2014 warner music uk limited\n23-Jun-14\ngoodbye to you (feat. dot rotten)\n5:30
loose change\ned sheeran\n 2010 all tracks (p) 2010 paw print records under exclusive license to warner music uk limited except for track 1 (p) 2011paw print records under exclusive license to warner music uk limited\n9-Dec-11\nfirefly (bravado dubstep remix)\n4:29
x\ned sheeran\n 2014 asylum records uk, a warner music uk company\n20-Jun-14\nafire love\n5:14
itunes festival: london 2012 - ep\ned sheeran\n 2012 warner music uk limited\n3-Sep-12\nthe a team (live)\n5:01
\.


--
-- Data for Name: left_tableaggregateright_tableaggregate_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.left_tableaggregateright_tableaggregate_table (word, synonym) FROM stdin;
\.


--
-- Data for Name: mercari_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercari_data (name, category) FROM stdin;
City color Be Matte Blush in Hibiscus	Beauty/Makeup/Face
Pageant Dress Slip	Kids/Girls (4+)/Dresses
New! VS Pink Bikini Top	Women/Swimwear/Two-Piece
Bring me the horizon posters	Home/Artwork/Posters & Prints
\.


--
-- Data for Name: right_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.right_table (aggregate) FROM stdin;
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nvhs outro (interlude) [explicit]\n1:25
title (deluxe)\nmeghan trainor\n 2011 what a music ltd, licence exclusive parlophone music france\n January 9, 2015\ncredit\n2:51
slow down remixes\nselena gomez\n (c) 2013 hollywood records, inc.\n August 20, 2013\nslow down (smash mode remix)\n5:21
good for you (remixes)\nselena gomez\n (c) 2015 interscope records\n September 4, 2015\ngood for you (yellow claw & cesqeaux remix) [feat. a$ap rocky]\n3:01
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nfirst show (interlude)\n0:11
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nvhs outro (interlude) [explicit]\n1:25
vhs [clean]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nmoving day (interlude)\n0:19
vhs \nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nvhs outro (interlude) \n1:26
vhs\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nvhs outro (interlude) \n1:25
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nsmoke (interlude) [explicit]\n0:24
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nsmoke (interlude) [explicit]\n0:24
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nsmoke (interlude) [explicit]\n0:24
the reason ep\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n August 10, 2015\nshining\n3:37
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\ny2k time capsule (interlude)\n0:32
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nsmoke (interlude) [explicit]\n0:24
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nmoving day (interlude)\n0:19
vhs [clean]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nmoving day (interlude)\n0:19
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nmoving day (interlude)\n0:19
vhs [clean]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nadam & noah's priorities (interlude)\n0:27
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nadam & noah's priorities (interlude)\n0:27
vhs [explicit]\nx ambassadors\n (c) 2015 kidinakorner/interscope records\n June 30, 2015\nmoving day (interlude)\n0:19
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nno one's here to sleep [feat. bastille] [explicit]\n4:32
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nwonder [feat. emeli sandê©]\n3:27
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\ntop floor (cabana) [feat. ed sheeran]\n2:09
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\npardon me [feat. tanika]\n2:50
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\none way [feat. mic righteous]\n3:26
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nwonder [feat. emeli sand©]\n3:27
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nthink about it [feat. wiz khalifa] [explicit]\n3:05
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nla la la [feat. sam smith]\n3:42
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nhollywood [feat. gabrielle]\n4:05
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nlifted [feat. emeli sand©]\n3:17
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nwonder [feat. emeli sandê©]\n3:27
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nso strong [feat. chasing grace]\n3:36
hotel cabana [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\npluto [feat. wretch 32]\n3:58
hotel cabana (deluxe version) [explicit]\nnaughty boy\n (c) 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n May 6, 2014\nnever been the same [feat. thabo]\n3:29
keep it goin' louder (maxi single) [explicit]\nmajor lazer\n (c) 2009 downtown music, llc. downtown records is a trademark of downtown music, llc.\n December 21, 2009\nkeep it goin' louder (savage skulls remix) [explicit]\n5:03
lean on (remixes)\nmajor lazer\n 2015 mad decent\n July 10, 2015\nlean on (fono remix) [feat. mó & dj snake]\n5:09
peace is the mission [explicit]\nmajor lazer\n 2015 mad decent\n June 1, 2015\nbe together (feat. wild belle)\n3:53
powerful (remixes)\nmajor lazer\n (c) 2015 third pardee records, llc under exclusive license to interscope records in the united states\n September 11, 2015\npowerful (michael calfan remix) [feat. ellie goulding]\n5:27
get it: hip-hop & pop for now [explicit]\nmajor lazer\n 2013 secretly canadian / mad decent\nnan\nbreak free [feat. zedd]\n3:34
nick jonas (deluxe) [clean]\nnick jonas\n (c) 2014 island records/safehouse records llc, a division of umg recordings, inc.\n November 10, 2014\nnumb [feat. angel haze] [clean]\n3:57
nick jonas (deluxe) [explicit]\nnick jonas\n (c) 2014 island records/safehouse records llc, a division of umg recordings, inc.\n November 10, 2014\nnothing would be better\n4:34
nick jonas (deluxe) [clean]\nnick jonas\n (c) 2014 island records/safehouse records llc, a division of umg recordings, inc.\n November 10, 2014\ncloser [feat. mike posner] [clean]\n3:48
nick jonas (deluxe) \nnick jonas\n (c) 2014 island records/safehouse records llc, a division of umg recordings, inc.\n November 10, 2014\ncloser [feat. mike posner] \n3:48
nick jonas \nnick jonas\n (c) 2014 island records/safehouse records llc, a division of umg recordings, inc.\n November 10, 2014\nnothing would be better\n4:34
#NAME?\ned sheeran\n doll records\n September 9, 2011\nsunburn \n4:35
5\ned sheeran\n dub police records\n June 23, 2014\nyou (+wiley)\n3:21
loose change\ned sheeran\n (c) 2007 geffen records/mosley music group llc\n December 9, 2011\nfirefly (bravado dubstep remix)\n4:29
x\ned sheeran\n (c) 2014 mau5trap recordings ltd\n June 20, 2014\nafire love\n5:14
the a team (ep)\ned sheeran\n sam hunt & david kilgour / bandit king records\n December 6, 2011\nthe a team\n4:18
\.


--
-- Data for Name: wherejio_smartitemsbeauty_comparison_beauty_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wherejio_smartitemsbeauty_comparison_beauty_table (word, synonym) FROM stdin;
Beauty	Flormar Quick Dry Nail Enamel QD20 Rose Taboo 11 ml
Beauty	mCaffeine Naked & Raw Moisturizing Coffee Body Lotion 200 ml
Beauty	Maryaj Deuce Homme EDP Spicy Woody Perfume And Ajmal Carbon Homme Deodorant Citrus Spicy Fragrance 300 ml
Beauty	O-Lens Spanish 1Day Coloured Contact Lenses - Grey ( 0.00 ) 1's
\.


--
-- Data for Name: wherejio_smartitemselectronics_comparison_electronics_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wherejio_smartitemselectronics_comparison_electronics_table (word, synonym) FROM stdin;
Electronics	EPSON T7741 Ink Bottle, Black
Electronics	Zebronics Zeb-Rocket Portable Bluetooth Wireless Speaker with AUX, USB, In-built FM radio
Electronics	EVM Enlarge 30000 mAh Power Bank, P0100
Electronics	Hanumex UV Protection Lens Filter (52 mm)
Electronics	Apple MU7E2ZM/A USB-C to 3.5 mm Headphone Jack Adapter
Electronics	SellZone Charger Adapter For Laptop Accer Spin 3
Electronics	SellZone Replacement Laptop Battery For Hp Pavilion Dv6-3050Tx(VIKBATTG0H01027)
\.


--
-- Data for Name: wherejio_smartitemsfashion_comparison_fashion_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wherejio_smartitemsfashion_comparison_fashion_table (word, synonym) FROM stdin;
Fashion	Flormar Quick Dry Nail Enamel QD20 Rose Taboo 11 ml
Fashion	Reliance Jewels Bal Gopal Ovel Gold 24 KT (999) 4 GM Coin
Fashion	mCaffeine Naked & Raw Moisturizing Coffee Body Lotion 200 ml
Fashion	Reliance Jewels Swastik Round Gold 24 KT (999) 4 GM Coin
Fashion	Maryaj Deuce Homme EDP Spicy Woody Perfume And Ajmal Carbon Homme Deodorant Citrus Spicy Fragrance 300 ml
Fashion	MarkQues Men's Watch and Genuine Leather Wallet Combo Gift Set for Men (BON-770909-VIN-4401)
Fashion	Viblitz Black Camera Belt
Fashion	O-Lens Spanish 1Day Coloured Contact Lenses - Grey ( 0.00 ) 1's
Fashion	BownBee Boys Green Printed Cotton Blend Kurta Sets
Fashion	Reliance Jewels Laxmi-Ganesh Gold 24 KT (999) 10 GM Coin
Fashion	Striped Dungaree Dress
\.


--
-- Data for Name: wherejio_smartitemsjewellery_comparison_jewellery_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wherejio_smartitemsjewellery_comparison_jewellery_table (word, synonym) FROM stdin;
Jewellery	Reliance Jewels Bal Gopal Ovel Gold 24 KT (999) 4 GM Coin
Jewellery	Reliance Jewels Swastik Round Gold 24 KT (999) 4 GM Coin
Jewellery	Reliance Jewels Laxmi-Ganesh Gold 24 KT (999) 10 GM Coin
\.


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

