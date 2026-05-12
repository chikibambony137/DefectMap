--
-- PostgreSQL database dump
--

\restrict tb7IfkK863zenOv1JlwFdvvDculQQ3uUvpgOMYKWITw973YuwLOvLFqHwL2gaiN

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

-- Started on 2026-05-01 15:53:55

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
-- TOC entry 4849 (class 0 OID 27184)
-- Dependencies: 217
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.alembic_version VALUES ('5c77bddfef71');


--
-- TOC entry 4853 (class 0 OID 27202)
-- Dependencies: 221
-- Data for Name: defect_criticality; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.defect_criticality VALUES (1, 'low', 1);
INSERT INTO public.defect_criticality VALUES (2, 'medium', 2);
INSERT INTO public.defect_criticality VALUES (3, 'high', 3);


--
-- TOC entry 4855 (class 0 OID 27211)
-- Dependencies: 223
-- Data for Name: defect_type; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.defect_type VALUES (1, 'electrical_failure', 'Электрическая неисправность');
INSERT INTO public.defect_type VALUES (2, 'mechanical_damage', 'Механическое повреждение');
INSERT INTO public.defect_type VALUES (3, 'calibration_error', 'Ошибка калибровки');
INSERT INTO public.defect_type VALUES (4, 'software_failure', 'Программный сбой');
INSERT INTO public.defect_type VALUES (5, 'display_failure', 'Неисправность дисплея');
INSERT INTO public.defect_type VALUES (6, 'battery_issue', 'Проблема с питанием');
INSERT INTO public.defect_type VALUES (7, 'other', 'Прочее');


--
-- TOC entry 4857 (class 0 OID 27223)
-- Dependencies: 225
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.equipment VALUES (1, 'SN001', 'Модель А', 'Завод 1', 'Москва, ул. Тверская, 1', 55.751574, 37.573856, '2023-01-15', 'active');
INSERT INTO public.equipment VALUES (2, 'SN002', 'Модель Б', 'Завод 2', 'Санкт-Петербург, Невский пр., 2', 59.93428, 30.335099, '2023-03-20', 'active');
INSERT INTO public.equipment VALUES (3, 'SN003', 'Модель А', 'Завод 1', 'Екатеринбург, ул. Ленина, 3', 56.838926, 60.597312, '2023-06-10', 'maintenance');
INSERT INTO public.equipment VALUES (4, 'SN004', 'Модель В', 'Завод 3', 'Новосибирск, Красный пр., 4', 55.030199, 82.92043, '2023-09-05', 'active');
INSERT INTO public.equipment VALUES (5, 'SN005', 'Модель Б', 'Завод 2', 'Казань, ул. Баумана, 5', 55.796127, 49.106405, '2024-01-25', 'decommissioned');
INSERT INTO public.equipment VALUES (6, 'SN006', 'Модель А', 'Завод 1', 'Нижний Новгород, ул. Большая Покровская, 6', 56.326797, 44.006516, '2024-02-14', 'active');
INSERT INTO public.equipment VALUES (7, 'SN007', 'Модель В', 'Завод 3', 'Челябинск, пр. Ленина, 7', 55.164441, 61.436843, '2024-03-01', 'active');
INSERT INTO public.equipment VALUES (8, 'SN008', 'Модель Б', 'Завод 2', 'Самара, ул. Куйбышева, 8', 53.195878, 50.100202, '2024-04-12', 'active');
INSERT INTO public.equipment VALUES (9, 'SN009', 'Модель А', 'Завод 1', 'Омск, пр. Мира, 9', 54.988482, 73.324236, '2024-05-20', 'active');
INSERT INTO public.equipment VALUES (10, 'SN010', 'Модель В', 'Завод 3', 'Ростов-на-Дону, ул. Большая Садовая, 10', 47.222078, 39.720358, '2024-06-30', 'active');


--
-- TOC entry 4859 (class 0 OID 27235)
-- Dependencies: 227
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.role OVERRIDING SYSTEM VALUE VALUES (1, 'admin');
INSERT INTO public.role OVERRIDING SYSTEM VALUE VALUES (2, 'engineer');
INSERT INTO public.role OVERRIDING SYSTEM VALUE VALUES (3, 'viewer');


--
-- TOC entry 4851 (class 0 OID 27190)
-- Dependencies: 219
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (1, 'Бряконогов', 'Иван', 'Иванович', 'ivanov', 'hash1', 1);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (2, 'Петров', 'Петр', 'Петрович', 'petrov', 'hash2', 2);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (3, 'Сидоров', 'Сидор', 'Сидорович', 'sidorov', 'hash3', 2);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (4, 'Козлова', 'Анна', 'Сергеевна', 'kozlovaa', 'hash4', 3);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (6, 'Бряконогов', 'Антон', 'Юрьевич', 'admin', '$2b$12$/su6BwS0MwEnb7LruWf9juShP86c/Y99mmhl/gx.6GeTEvAbXPwom', 1);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (5, 'Винниченко', 'Кирилл', 'Антонович', 'string', '$2b$12$1prAtyOQScDFaztBZjr2/O1hzmDvXfBGtj35VNtgV3HEKuCCYkbIe', 3);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (7, 'Сизов', 'Евгений', 'Олегович', 'creeper2004', '$2b$12$WrgbFTGAH2GuVbPUofbgiucliOpQsym4kO7yYe9lA1tRbx88NLppi', 3);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (8, 'string', 'string', NULL, 'string1', '$2b$12$CKspjlX4lebrm5YOAgproO0jJpK2kGEfux4eAelRavwHMqLKYvavu', 3);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (9, 'Лябахов', 'Арсений', 'Крутович', '12345', '$2b$12$53ZCicR.WwIyCkz.STywB.SxHDRh6NzhiSMHGpoZxp4yZm9Yto2gW', 3);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (10, 'Лябахов', 'Арсений', 'Крутович', '123456', '$2b$12$8GkyYqGSJ2ToQ9TLWW1qYuxM5Zd7.4otMUDq1LUfLKvvafbuzEo42', 3);
INSERT INTO public."user" OVERRIDING SYSTEM VALUE VALUES (11, 'Самыгин', 'Глеб', 'Прайдович', '1234', '$2b$12$ENM7Ftwqq9mRL8MqMEyolONbNPu82U/HawnhvuCkaPtY6AQiW.3.a', 3);


--
-- TOC entry 4861 (class 0 OID 27243)
-- Dependencies: 229
-- Data for Name: defect; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.defect VALUES (11, 'Не включается', 'Прибор не реагирует на кнопку включения', 'open', '2025-01-10 10:30:00', NULL, NULL, 3, 1, 2, 1);
INSERT INTO public.defect VALUES (12, 'Ошибка измерения', 'Показывает некорректные значения', 'in_progress', '2025-01-15 14:20:00', NULL, NULL, 2, 2, 2, 3);
INSERT INTO public.defect VALUES (13, 'Треснул корпус', 'Механическое повреждение корпуса', 'closed', '2025-01-05 09:00:00', '2025-01-20 16:30:00', 'https://example.com/photo1.jpg', 1, 3, 2, 2);
INSERT INTO public.defect VALUES (14, 'Зависает при запуске', 'Зависает на логотипе', 'open', '2025-02-01 11:45:00', NULL, NULL, 2, 4, 3, 4);
INSERT INTO public.defect VALUES (15, 'Не заряжается', 'Не берёт заряд от сети', 'in_progress', '2025-02-05 08:15:00', NULL, NULL, 3, 5, 3, 6);
INSERT INTO public.defect VALUES (16, 'Пропадает изображение', 'Экран моргает и гаснет', 'open', '2025-02-10 13:00:00', NULL, NULL, 2, 6, 2, 5);
INSERT INTO public.defect VALUES (17, 'Проблема с подключением', 'Не видит внешние устройства', 'closed', '2025-01-20 10:00:00', '2025-02-12 14:20:00', NULL, 1, 7, 2, 7);
INSERT INTO public.defect VALUES (18, 'Шумит при работе', 'Издаёт посторонние звуки', 'open', '2025-02-15 09:30:00', NULL, NULL, 1, 8, 3, 2);
INSERT INTO public.defect VALUES (19, 'Сброс настроек', 'Стирает настройки после выключения', 'in_progress', '2025-02-18 16:45:00', NULL, NULL, 2, 9, 2, 4);
INSERT INTO public.defect VALUES (20, 'Ошибка калибровки', 'Не проходит процедуру калибровки', 'open', '2025-02-20 12:00:00', NULL, NULL, 3, 10, 3, 3);


--
-- TOC entry 4869 (class 0 OID 0)
-- Dependencies: 220
-- Name: defect_criticality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.defect_criticality_id_seq', 3, true);


--
-- TOC entry 4870 (class 0 OID 0)
-- Dependencies: 228
-- Name: defect_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.defect_id_seq', 20, true);


--
-- TOC entry 4871 (class 0 OID 0)
-- Dependencies: 222
-- Name: defect_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.defect_type_id_seq', 7, true);


--
-- TOC entry 4872 (class 0 OID 0)
-- Dependencies: 224
-- Name: equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.equipment_id_seq', 10, true);


--
-- TOC entry 4873 (class 0 OID 0)
-- Dependencies: 226
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.role_id_seq', 9, true);


--
-- TOC entry 4874 (class 0 OID 0)
-- Dependencies: 231
-- Name: role_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.role_id_seq1', 4, false);


--
-- TOC entry 4875 (class 0 OID 0)
-- Dependencies: 218
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 16, true);


--
-- TOC entry 4876 (class 0 OID 0)
-- Dependencies: 230
-- Name: user_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq1', 11, true);


-- Completed on 2026-05-01 15:53:55

--
-- PostgreSQL database dump complete
--

\unrestrict tb7IfkK863zenOv1JlwFdvvDculQQ3uUvpgOMYKWITw973YuwLOvLFqHwL2gaiN

