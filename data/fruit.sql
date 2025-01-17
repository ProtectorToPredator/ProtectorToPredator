--
-- PostgreSQL database dump
--

-- Dumped from database version 10.23 (Ubuntu 10.23-0ubuntu0.18.04.2)
-- Dumped by pg_dump version 10.23 (Ubuntu 10.23-0ubuntu0.18.04.2)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: encdb; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS encdb WITH SCHEMA public;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: fruit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fruit (
    fruit_id integer,
    name text,
    quantity public.enc_int4
);


ALTER TABLE public.fruit OWNER TO postgres;

--
-- Data for Name: fruit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fruit (fruit_id, name, quantity) FROM stdin;
1	Apple	l9g9v9VzlLQfKfkizLwmq2XVjjy8OZvRHBPRRYOSpsX=
2	Banana	ZtjUCdcchQKqoty/3Z+k0+km4ERTWQjRki0CerYQutj=
3	Cherry	ocDlW2uMcmFtZYCLs4YuJ+qI6BfW8PfyaVzx2T0aFmb=
4	Orange	BbHBY8XjYvYDC0E2WEN8wYD9v+JoiqLM+z7gRIoAXkr=
5	Grape	QCgHaSC4eWwFceWR/+9fIaoE81h/juF5boR8V3ZzMpj=
6	Mango	9UvZvBc9v3bB064kweGslb8zaCijG8b83SInqMjotIP=
7	Pineapple	6lEUqjGZR/+QrzqHG/x6SZ/aGExiyFQ7PdYgmXSYmcf=
8	Strawberry	YD53vOryrBOhnPVHAxfUdBfQN32Mf/UNpVC4d1uAKkz=
9	Watermelon	pGDpVzp7LcghFUNV63sOldbdforv5k/ARvM/L5ROga3=
10	Kiwi	fehqjWIieOd6PUjgDiyKfODuIQbIAwIDUcPRWSgkBbr=
11	Peach	EUJJ/8w2zMOWy+iGmX9iTfRoCa/6utZsxe4Cvwu25Hb=
12	Pear	7m3LqTQQAhLFXG5OZFhzSzeyiA2c00yBRkzDi3wHpP3=
\.


--
-- PostgreSQL database dump complete
--

