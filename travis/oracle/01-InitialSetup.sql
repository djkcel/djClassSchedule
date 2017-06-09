-- Initial Database Setup For Testing

CREATE TABLE SWVPTRM_UP_WEB (
      TERM VARCHAR2(100),
      PTRM VARCHAR2(100),
      PTRM_DESC VARCHAR2(200),
      PTRM_START DATE,
      PTRM_END DATE
);

INSERT INTO SWVPTRM_UP_WEB VALUES ('201520', 'R4', 'Fun Term', sysdate, sysdate + 100);
INSERT INTO SWVPTRM_UP_WEB VALUES ('201525', 'P3', 'P Term', sysdate, sysdate + 100);

exit