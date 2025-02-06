# lunch-menu
- [x] 팀원들의 점심 메뉴를 수집
- [x] 분석
- [ ] 알람(입력하지 않은 사람들에게 ...)
- [ ] CSV to DB

## Ready
### Install DB with Docker
```bash
$ sudo docker run --name local-postgres \
-e POSTGRES_USER=sunsin \
-e POSTGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432 \
-d postgres:15.10
```

### Create Table
- postgres
```sql
CREATE TABLE public.lunch_menu (
	id serial NOT NULL,
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)
);

alter table lunch_menu
add constraint unique_member_dt unique (member_name, dt);

create table member(
id serial NOT NULL,
name text unique NOT NULL
);

select * from member;

insert into member(name)
values 
('TOM'),
('cho'),
('hyun'),
('JERRY'),
('SEO'),
('jiwon'),
('jacob'),
('heejin'),
('lucas'),
('nuni')
;

select * from member;

select jsonb_object_agg(name, id)
from ( 
	select name, id from member order by id
) temp;

--새로운 컬럼 추가
alter table lunch_menu 
add column member_id int;

select * from lunch_menu limit 1;

--기존의 제약조건을 삭제
alter table lunch_menu
drop constraint unique_member_dt;

-- 사용하지 않는 컬럼 삭제
alter table lunch_menu
drop column member_name;

--member_id null 값을 허용하지 않도록 설정
--delete from lunch_menu
alter table lunch_menu
alter column member_id set not null;

select * from lunch_menu;

-- 새로운 제약조건 추가
alter table lunch_menu
add constraint unique_memberid_dt unique(member_id, dt);

-- 멤버 테이블에 기본키를 설정: 기본 키가 있어야 참조키를 설정할 수 있다고 함
alter table member
add constraint member_id_pk primary key(id);

-- 관계 조건 추가
alter table lunch_menu
add constraint menu_member_fk 
	foreign key (member_id)
	references member(id)

```

## Dev
- DB
```bash
$ sudo docker ps -a
$ sudo docker start local-postgres
$ sudo docker stop local-postgres

# Into CONTAINER
$ sudo docker exec -it local-postgres bash
```

- RUN
```bash
# 디비 정보에 맞춰 수정
$ cp env.dummy .env

# 서버 시작
$ streamlit run App.py
```
