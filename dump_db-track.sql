--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--

DROP DATABASE fastapi_track;




--
-- Drop roles
--

DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:SMR/Oc+NsCtNmVQ9CchH1A==$aLYL1iUHziLpHECZuuEWZSaUN86jk8e/D94RUUnb3D4=:HDSaEfBbK+10qUK9Fd8OGjx0eukRRv4KO0kMdt/keq0=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Debian 15.1-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO postgres;

\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: postgres
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: postgres
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- Database "fastapi_track" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Debian 15.1-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: fastapi_track; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE fastapi_track WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE fastapi_track OWNER TO postgres;

\connect fastapi_track

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Blog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Blog" (
    title character varying NOT NULL,
    file_name character varying NOT NULL,
    file_url character varying NOT NULL,
    type character varying NOT NULL,
    id integer NOT NULL,
    updated_at timestamp without time zone,
    created_at timestamp without time zone,
    link character varying,
    hashtag character varying,
    description character varying
);


ALTER TABLE public."Blog" OWNER TO postgres;

--
-- Name: Blog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Blog_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Blog_id_seq" OWNER TO postgres;

--
-- Name: Blog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Blog_id_seq" OWNED BY public."Blog".id;


--
-- Name: Comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Comment" (
    your_name character varying NOT NULL,
    company_name character varying NOT NULL,
    email_address character varying NOT NULL,
    phone_number character varying NOT NULL,
    comment character varying NOT NULL,
    id integer NOT NULL,
    updated_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public."Comment" OWNER TO postgres;

--
-- Name: Comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Comment_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Comment_id_seq" OWNER TO postgres;

--
-- Name: Comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Comment_id_seq" OWNED BY public."Comment".id;


--
-- Name: ImageMedia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ImageMedia" (
    file_name character varying,
    file_content character varying,
    file_ext character varying NOT NULL,
    id integer NOT NULL,
    updated_at timestamp without time zone,
    created_at timestamp without time zone,
    track_id integer
);


ALTER TABLE public."ImageMedia" OWNER TO postgres;

--
-- Name: ImageMedia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ImageMedia_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ImageMedia_id_seq" OWNER TO postgres;

--
-- Name: ImageMedia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ImageMedia_id_seq" OWNED BY public."ImageMedia".id;


--
-- Name: Role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Role" (
    name character varying NOT NULL,
    description character varying NOT NULL,
    id integer NOT NULL,
    updated_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public."Role" OWNER TO postgres;

--
-- Name: Role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Role_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Role_id_seq" OWNER TO postgres;

--
-- Name: Role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Role_id_seq" OWNED BY public."Role".id;


--
-- Name: Track; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Track" (
    name character varying NOT NULL,
    description character varying NOT NULL,
    price integer NOT NULL,
    is_active boolean NOT NULL,
    id integer NOT NULL,
    updated_at timestamp without time zone,
    created_at timestamp without time zone,
    created_by_id integer
);


ALTER TABLE public."Track" OWNER TO postgres;

--
-- Name: Track_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Track_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Track_id_seq" OWNER TO postgres;

--
-- Name: Track_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Track_id_seq" OWNED BY public."Track".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    birthdate timestamp with time zone,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    role_id integer,
    phone character varying,
    id integer NOT NULL,
    updated_at timestamp without time zone,
    created_at timestamp without time zone,
    hashed_password character varying NOT NULL
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_id_seq" OWNER TO postgres;

--
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: Blog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Blog" ALTER COLUMN id SET DEFAULT nextval('public."Blog_id_seq"'::regclass);


--
-- Name: Comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Comment" ALTER COLUMN id SET DEFAULT nextval('public."Comment_id_seq"'::regclass);


--
-- Name: ImageMedia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ImageMedia" ALTER COLUMN id SET DEFAULT nextval('public."ImageMedia_id_seq"'::regclass);


--
-- Name: Role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Role" ALTER COLUMN id SET DEFAULT nextval('public."Role_id_seq"'::regclass);


--
-- Name: Track id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Track" ALTER COLUMN id SET DEFAULT nextval('public."Track_id_seq"'::regclass);


--
-- Name: User id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- Data for Name: Blog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Blog" (title, file_name, file_url, type, id, updated_at, created_at, link, hashtag, description) FROM stdin;
New Car	2d0f13b0f3cbc7d7fec3.png	/static/images/2d0f13b0f3cbc7d7fec3.png	1	7	2023-02-16 12:54:28.45074	2023-02-16 12:54:28.450742	https://www.instagram.com/	#new#instagram	New Car desc
test123	ae71cf9f5752c1482bec.avif	/static/images/ae71cf9f5752c1482bec.avif	1	8	2023-02-16 12:57:19.913886	2023-02-16 12:56:43.33816	https://www.facebook.com/watch	#news#nimadir	test test test
errere	0f766f101fac9834eb80.png	/static/images/0f766f101fac9834eb80.png	1	9	2023-02-16 13:09:43.343945	2023-02-16 13:09:43.343948	google.com	#news#nimadir#goo	ererer
ttttt	52c63e2bcd1fb6af84d4.png	/static/images/52c63e2bcd1fb6af84d4.png	1	10	2023-02-16 13:10:21.940214	2023-02-16 13:10:21.940216	google.com	#success#news#nimadir	rtertert
\.


--
-- Data for Name: Comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Comment" (your_name, company_name, email_address, phone_number, comment, id, updated_at, created_at) FROM stdin;
John Doe	John Doe	johndoe@example.com	998900711313	Hello. My name is John Doe. I'm a founder of JohnDoe.	1	2023-02-10 10:31:44.510752	2023-02-10 10:31:44.510758
Ahror Sulaymanov	company	ahrorsulaymanov2@gmail.com	+998930085504	comment  comment  comment comment 	2	2023-02-10 14:15:48.258091	2023-02-10 14:15:48.258095
Ahror Sulaymanov	company	ahrorsulaymanov2@gmail.com	+998930085504	d5rft4rter	4	2023-02-18 10:39:05.87093	2023-02-18 10:39:05.870959
\.


--
-- Data for Name: ImageMedia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ImageMedia" (file_name, file_content, file_ext, id, updated_at, created_at, track_id) FROM stdin;
/static/images/614dd457d9644b519ffb.png	3f426eb16103bd9eaac17de2ee8db6de83f0a4e14c80e85d27d133831da727a1	png	78	2023-02-10 13:14:59.699986	2023-02-10 13:14:59.699989	57
/static/images/ba9356e2c5eda547d502.png	b1357423b0f507ac6191b7fcd7e96e7ea0583c43817b41163cda7f1825426a85	png	79	2023-02-10 13:14:59.726764	2023-02-10 13:14:59.726766	57
/static/images/169a385aaa1e78e98798.png	29594979911110d111698d351abafb86fb6f99962c2c58e8b38897ce31384a18	png	80	2023-02-10 13:14:59.736641	2023-02-10 13:14:59.736643	57
/static/images/3da3acf6fabc0f508233.png	b445d154843b4e0d7e15e1be58aca1a92e2875afe762772c308b661922143b36	png	81	2023-02-10 13:19:18.960172	2023-02-10 13:19:18.960189	58
/static/images/c9dd9c79e464d0f66cec.png	bbebcabfd820a855aa5c81dddc3cc66f95e7977b4e1a0a58ba1a72768c9a8d43	png	82	2023-02-10 13:19:18.967399	2023-02-10 13:19:18.967402	58
/static/images/3bafb94c2a3b54821cfe.png	d4afe6859750144da75bf70291fe6a4008f311a432720df96e2cad8eb6c4bc11	png	83	2023-02-10 13:19:18.972956	2023-02-10 13:19:18.972957	58
/static/images/3de6f1aeabf655e65311.png	b1eba60f9257c6d496063bfa2f6b5600bd36d616d96d433e8c800787870fe14a	png	84	2023-02-10 13:21:09.349585	2023-02-10 13:21:09.349587	59
/static/images/aea67344666fec9274c3.png	b65c5b6e0b803dd317085a84b4caf167017bb6f2dbb8ef07a67858674866a6e1	png	85	2023-02-10 13:21:09.35835	2023-02-10 13:21:09.358352	59
/static/images/421afea07a5969ec57c7.png	794f48f32e33e28ab29be2c35c8f4412e2de5ff76e3b9f88d5282742381469fa	png	86	2023-02-10 13:21:09.363742	2023-02-10 13:21:09.363745	59
/static/images/283ec82a7ef229778cce.png	63cd6b23acc1171ce97a2a267941709280c55fa90297bf727ee8392a4159646c	png	87	2023-02-10 13:23:46.378561	2023-02-10 13:23:46.378563	60
/static/images/2aafaf8b03725933ef54.png	22e10d41c1a4a481fbadeef4f9ee79ca64b18295a3948a46c81afb098ba69c84	png	88	2023-02-10 13:23:46.385301	2023-02-10 13:23:46.385303	60
Screenshot_20221124_111752.png	5c97c9a54a62594e8ac65bf1d739596f96b0e26b116f90162bbddaa410621ecc	png	6	2023-02-08 12:19:16.992726	2023-02-03 14:33:07.752285	\N
Screenshot_20221124_050428.png	d59983507c76a040938103d03c84157926875a8057a93c82b357f630484977d2	png	3	2023-02-08 12:26:34.393292	2023-02-03 14:03:33.242657	\N
/static/images/7d156707ac9acaec9471.png	c1a429458c75b83ad689fa2a19d01c57af426db77a69097dfb335b70db632b79	png	89	2023-02-10 13:23:46.389876	2023-02-10 13:23:46.389877	60
acer01.jpg	b9115d3374b1d8e375d829ac13d3435c005f7a0203975885a97a2525478edb7e	jpg	2	2023-02-08 12:37:10.67896	2023-02-03 13:47:06.49844	\N
IMG_20211217_184325.jpg	cc583f35e686ae8afb0ded74182b8d324f397815b391a8583578d776c1c75a0d	jpg	1	2023-02-08 12:46:11.355189	2023-02-03 13:39:56.162509	\N
/static/images/b64a35b9304be093a845.png	8e78810e5746ad638f41f9c820f8f35fc4903ebb13fdad46305b94b36a0cfa3b	png	90	2023-02-10 13:25:39.717597	2023-02-10 13:25:39.717599	61
/static/images/a1e7ebf1001fc4b18708.png	944def2e05d65abdb03cf9ece877a8ea90a4fc047f8a86394dd1bf6916f44d6d	png	91	2023-02-10 13:25:39.72343	2023-02-10 13:25:39.723433	61
/static/images/89b9e907eaec1dbc8e06.png	411c0ccb3c27bceaa53787a7deb69d67f2c1f00648c99c86406f503488d659b0	png	92	2023-02-10 13:25:39.728438	2023-02-10 13:25:39.728442	61
/static/images/5b00703b852cca026dae.png	b1400b642ff2fd538a387add20ac9fffbaf55f031665f5a57fd85111b457b53a	png	93	2023-02-10 13:27:04.919028	2023-02-10 13:27:04.919032	62
/static/images/414a0862852f3e55e3a7.png	6f29e552777d1b50578222a0eb88865c5fb7ded63be424239d6baee762cf2c37	png	94	2023-02-10 13:27:04.927916	2023-02-10 13:27:04.927919	62
/static/images/5a14029dec94989c968a.png	c97216fb765a8e52b35d5789c59ca58aa2499d412ce39c154d70418f263ff334	png	95	2023-02-10 13:27:04.936131	2023-02-10 13:27:04.936133	62
/static/images/01d0f73d40ade5742898.png	1fd3ace79b2a5222b2a099801f97c04d6f4ce1f2219f7d251968f8fa481e989b	png	96	2023-02-10 13:28:24.177028	2023-02-10 13:28:24.177031	63
/static/images/722a389f55ad50b63ebd.png	cdeacd44da72e61800c61cbe4124fc40a7f48f660b5ec9b835b835cd1f3ade2a	png	97	2023-02-10 13:28:24.183198	2023-02-10 13:28:24.1832	63
/static/images/6e637fe3dfa7cef4b262.png	72759445838b0744e07c8864c58bba168cffce2e461d4c621e8bb40608a2abaf	png	98	2023-02-10 13:28:24.189375	2023-02-10 13:28:24.189377	63
/static/images/e2c06c667a1234aa494b.png	68cb60f31bdedbf2513d036e09aeed37ffeeb7947afbe0385e16a97669656992	png	99	2023-02-10 13:29:28.249768	2023-02-10 13:29:28.24977	64
/static/images/b14ac6d60efb46023373.png	ead1104a0d53d522e35779afc17edd162e0c51929ea8ec367cbca5352af8cd59	png	100	2023-02-10 13:29:28.25598	2023-02-10 13:29:28.255983	64
/static/images/4cfee3f5c3a4cabadbcf.png	a00bef8667529bb9ba0396a95b7b8964e66f72cf42945e2f1737a81e8bc2df13	png	101	2023-02-10 13:29:28.261206	2023-02-10 13:29:28.261208	64
\.


--
-- Data for Name: Role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Role" (name, description, id, updated_at, created_at) FROM stdin;
admin	This the Admin role	1	2023-01-29 19:07:35.22832	2023-01-29 19:07:35.228323
manager	Manager role	2	2023-01-29 19:07:35.285089	2023-01-29 19:07:35.285091
user	User role	3	2023-01-29 19:07:35.309349	2023-01-29 19:07:35.309352
\.


--
-- Data for Name: Track; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Track" (name, description, price, is_active, id, updated_at, created_at, created_by_id) FROM stdin;
Freightliner 2020	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	t	57	2023-02-10 13:14:59.560871	2023-02-10 13:14:59.560874	1
Freightliner 2021	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	t	59	2023-02-10 13:21:09.308097	2023-02-10 13:21:09.308099	1
Kenworth 2022	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	f	60	2023-02-10 13:23:46.337679	2023-02-10 13:23:46.337681	1
Freightlienr 2022	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	f	58	2023-02-10 13:23:48.306263	2023-02-10 13:19:18.905529	1
Kenworth 2020	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	t	61	2023-02-10 13:25:39.670703	2023-02-10 13:25:39.670705	1
Volvo 860 2022	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	t	62	2023-02-10 14:46:52.962964	2023-02-10 13:27:04.868711	1
Volvo 760 2020	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	t	63	2023-02-18 10:50:16.169588	2023-02-10 13:28:24.137987	1
Volvo 760 2022	Lorem ipsum dolor sit amet consectetur. Eget at enim fermentum id.	100000	t	64	2023-02-18 10:51:19.227188	2023-02-10 13:29:28.206764	1
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."User" (birthdate, first_name, last_name, email, is_active, is_superuser, role_id, phone, id, updated_at, created_at, hashed_password) FROM stdin;
\N	Manager	Manager aka	manager@example.com	t	f	2	+998900711313	2	2023-01-29 19:07:35.626344	2023-01-29 19:07:35.626347	$2b$12$sN5nzJ8E4zSNhs633Y1SkeZzib6KfifdUgmhsFf3MH59GP3PvIkuu
\N	User	Userjon	user@example.com	t	f	3	+998919713733	3	2023-01-29 19:07:35.882738	2023-01-29 19:07:35.882739	$2b$12$EjnN2CdwtoW7iTPmH4oDDOnPm2ERKXY.1QcwlAgW5yRJItkDO6NaG
2023-02-04 10:00:12.462+00	string	string	user2@example.com	t	t	2	+998919791999	4	2023-02-04 10:01:12.171046	2023-02-04 10:01:12.171052	$2b$12$RyxgkwWQ9MP5bAL0D2bVr.cjpGQ2RnnGpQzHEEgMitUNjsQfAuWDq
\N	Admin	Katta Bola	admin@admin.com	t	t	1	+998903470113	1	2023-02-18 10:29:31.877727	2023-01-29 19:07:35.338044	$2b$12$4ISEkjB/m6PD05nijePkrunQ8BXGcLNGH5Wzb6LdJbdQpYGMIoSAa
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
9ba1452dc30f
\.


--
-- Name: Blog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Blog_id_seq"', 10, true);


--
-- Name: Comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Comment_id_seq"', 4, true);


--
-- Name: ImageMedia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."ImageMedia_id_seq"', 101, true);


--
-- Name: Role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Role_id_seq"', 3, true);


--
-- Name: Track_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Track_id_seq"', 64, true);


--
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_id_seq"', 4, true);


--
-- Name: Blog Blog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Blog"
    ADD CONSTRAINT "Blog_pkey" PRIMARY KEY (id);


--
-- Name: Comment Comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Comment"
    ADD CONSTRAINT "Comment_pkey" PRIMARY KEY (id);


--
-- Name: ImageMedia ImageMedia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ImageMedia"
    ADD CONSTRAINT "ImageMedia_pkey" PRIMARY KEY (id);


--
-- Name: Role Role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Role"
    ADD CONSTRAINT "Role_pkey" PRIMARY KEY (id);


--
-- Name: Track Track_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Track"
    ADD CONSTRAINT "Track_pkey" PRIMARY KEY (id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: ix_Track_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_Track_name" ON public."Track" USING btree (name);


--
-- Name: ix_User_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX "ix_User_email" ON public."User" USING btree (email);


--
-- Name: ix_User_hashed_password; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_User_hashed_password" ON public."User" USING btree (hashed_password);


--
-- Name: ix_User_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX "ix_User_phone" ON public."User" USING btree (phone);


--
-- Name: ImageMedia ImageMedia_track_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ImageMedia"
    ADD CONSTRAINT "ImageMedia_track_id_fkey" FOREIGN KEY (track_id) REFERENCES public."Track"(id) ON DELETE CASCADE;


--
-- Name: Track Track_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Track"
    ADD CONSTRAINT "Track_created_by_id_fkey" FOREIGN KEY (created_by_id) REFERENCES public."User"(id);


--
-- Name: User User_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_role_id_fkey" FOREIGN KEY (role_id) REFERENCES public."Role"(id);


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Debian 15.1-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO postgres;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

