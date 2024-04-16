CREATE DATABASE diplom
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE public.category
(
    id bigint NOT NULL DEFAULT nextval('category_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    user_id bigint,
    CONSTRAINT category_pkey PRIMARY KEY (id),
    CONSTRAINT category_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE public.category_profit
(
    id bigint NOT NULL DEFAULT nextval('category_profit_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    user_id bigint,
    CONSTRAINT category_profit_pkey PRIMARY KEY (id),
    CONSTRAINT category_profit_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE public.main
(
    id bigint NOT NULL DEFAULT nextval('main_id_seq'::regclass),
    user_id bigint,
    shop bigint,
    category bigint,
    date date,
    sum double precision,
    CONSTRAINT main_pkey PRIMARY KEY (id),
    CONSTRAINT category FOREIGN KEY (category)
        REFERENCES public.category (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT shop FOREIGN KEY (shop)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT "user" FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE public.profit_main
(
    id bigint NOT NULL DEFAULT nextval('profit_main_id_seq'::regclass),
    user_id bigint,
    category_profit bigint,
    date date,
    sum double precision,
    CONSTRAINT profit_main_pkey PRIMARY KEY (id),
    CONSTRAINT profit_main_category_profit_fkey FOREIGN KEY (category_profit)
        REFERENCES public.category_profit (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT profit_main_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE public.shops
(
    id bigint NOT NULL DEFAULT nextval('shops_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    user_id bigint,
    CONSTRAINT shops_pkey PRIMARY KEY (id),
    CONSTRAINT shops_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE public.users
(
    id bigint NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    login character varying COLLATE pg_catalog."default",
    pass character varying COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id)
);