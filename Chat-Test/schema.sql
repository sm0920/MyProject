drop table if exists chatLog;
create table chatLog
(
	sequence integer primary key autoincrement,
	name string not null,
	text string not null
);
