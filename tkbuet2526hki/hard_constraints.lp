% ====== DOMAIN & FACTS ======
d(0..D-1)   :- days(D).
ppd(0..P-1) :- periods_per_day(P).

r(R)  :- room(R,_,_,_).
c(S)  :- course(S,_,_,_).
t(T)  :- lecturer(T,_,_).
cl(CL):- class_course(_,CL).
mr(MR):- mandatory_room(_,MR).

course_id(S, CID, Type) :- course(S, CID, Type, _).

% =========================================================

room_building(R, B) :- room(R,_,_,B).                   
% --- room_building(R, R) :- mandatory_room(_, R), not room(R, _, _, _). ---

% 1. Xác định phòng hợp lệ cho từng môn 
valid_room(S, R) :- mandatory_room(S, R).
valid_room(S, R) :- not mandatory_room(S, _), course(S,_,_,Size), room(R,_,Cap,_), Cap >= Size.

% 2. Xác định các cặp môn "Nguy hiểm" (Cần kiểm tra đổi tòa nhà)
pair_teacher(S1, S2) :- teacher_course(S1, T), teacher_course(S2, T), S1 != S2, S1 < S2.
pair_class(S1, S2)   :- class_course(S1, C), class_course(S2, C), S1 != S2, S1 < S2.

% =========================================================

% 1. Gán Timeslot (Giữ nguyên vì miền thời gian nhỏ)
1 { ts(S,D,P) : d(D), ppd(P) } 1 :- c(S).

% 2. Gán Phòng (TỐI ƯU: Chỉ gán vào phòng trong valid_room)
1 { assigned(S,R,D,P) : valid_room(S,R) } 1 :- ts(S,D,P).

% =========================================================

:- t(T), d(D), ppd(P), 2 { ts(S,D,P) : teacher_course(S,T) }.

:- cl(CL), d(D), ppd(P), 2 { ts(S,D,P) : class_course(S,CL) }.

:- mr(MR), d(D), ppd(P), 2 { ts(S,D,P) : mandatory_room(S,MR) }.

:- d(D), course_details(_, CID, Type), 
   2 { ts(S, D, _) : course_details(S, CID, Type) }.

% Ý nghĩa: Tại một phòng R, giờ D, P không được có quá 1 môn
:- r(R), d(D), ppd(P), 2 { assigned(S,R,D,P) }.

% Chỉ tạo luật cấm cho các cặp pair_teacher đã tính trước
:- pair_teacher(S1, S2),                
   ts(S1, D, P), ts(S2, D, P+1),        
   assigned(S1, R1, D, P),              
   assigned(S2, R2, D, P+1),            
   room_building(R1,B1), room_building(R2,B2),    
   B1 != B2.

:- pair_teacher(S1, S2),                
   ts(S1, D, P+1), ts(S2, D, P),        
   assigned(S1, R1, D, P+1),              
   assigned(S2, R2, D, P),            
   room_building(R1,B1), room_building(R2,B2),    
   B1 != B2.                      

% Tương tự, chỉ xét cặp pair_class
:- pair_class(S1, S2),
   ts(S1, D, P), ts(S2, D, P+1),
   assigned(S1, R1, D, P), 
   assigned(S2, R2, D, P+1),
   room_building(R1,B1), room_building(R2,B2),
   B1 != B2.

:- pair_class(S1, S2),
   ts(S1, D, P+1), ts(S2, D, P),
   assigned(S1, R1, D, P+1), 
   assigned(S2, R2, D, P),
   room_building(R1,B1), room_building(R2,B2),
   B1 != B2.

#show assigned/4.