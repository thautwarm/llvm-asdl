

@_ZTVN10__cxxabiv117__class_type_infoE = external global i8*

@_ZTS1S = linkonce_odr constant [3 x i8] c"2S\00"

%.merlin.type.S = type { i32, i32, double }

@str = private unnamed_addr constant [3 x i8] c"ok\00"

@.S.resume.inst = linkonce_odr constant { i8*, i8* }
									{ i8* bitcast (i8** getelementptr (i8*, i8** @_ZTVN10__cxxabiv117__class_type_infoE, i64 2) to i8*),
										i8* getelementptr inbounds ([3 x i8], [3 x i8]* @_ZTS1S, i32 0, i32 0) }

@.inst = private unnamed_addr constant %.merlin.type.S { i32 1, i32 1, double 1.0 }, align 8

define i32 @main() personality i8* bitcast (i32 (...)* @__gxx_personality_v0 to i8*) {


Entry:
	%local.exc.body = tail call i8* @__cxa_allocate_exception(i64 16)
	call void @llvm.memcpy.p0i8.p0i8.i64(i8* %local.exc.body , i8* bitcast (%.merlin.type.S* @.inst to i8*), i64 16, i32 8, i1 false)
	invoke void @__cxa_throw(i8* %local.exc.body, i8* bitcast ( { i8*, i8* }* @.S.resume.inst to i8*), i8* null)
			to label %LocalExtNo unwind label %LocalExt

LocalExtNo:
	ret i32 0

LocalExt:
	%local.exc1.catched = landingpad { i8*, i32 }
							catch i8* bitcast ({ i8*, i8* }* @.S.resume.inst to i8*)

	%local.exc1.catched.typeid = extractvalue { i8*, i32 } %local.exc1.catched, 1

	%local.exc1.catched.typeid.expected = tail call i32
					@llvm.eh.typeid.for(i8* bitcast ({ i8*, i8* }* @.S.resume.inst to i8*))

	%.local.exc1.test_match = icmp eq i32 %local.exc1.catched.typeid, %local.exc1.catched.typeid.expected

	br i1 %.local.exc1.test_match, label %LocalExtGoAhead, label %LocalExtResume


LocalExtResume:
	resume {i8*, i32} %local.exc1.catched

LocalExtUnreachable:
	unreachable

LocalExtGoAhead:
	%.local.exc1.metainfo = extractvalue { i8*, i32 } %local.exc1.catched, 0
	%.local.tmp = tail call i8* @__cxa_begin_catch(i8* %.local.exc1.metainfo)
	tail call i32 (i8*, ...) @printf(i8* getelementptr ([3 x i8], [3 x i8]* @str, i64 0, i64 0))
	tail call void @__cxa_end_catch()
	br label %LocalExtNo

}

declare i32 @__gxx_personality_v0(...)


declare i8* @__cxa_allocate_exception(i64) local_unnamed_addr

declare void @__cxa_throw(i8*, i8*, i8*) local_unnamed_addr

declare i8* @__cxa_begin_catch(i8*) local_unnamed_addr

declare void @__cxa_end_catch() local_unnamed_addr

declare i32 @printf(i8* nocapture readonly, ...) local_unnamed_addr

declare i32 @llvm.eh.typeid.for(i8*)

declare void @llvm.memcpy.p0i8.p0i8.i64(i8*, i8*, i64, i32, i1)

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 6.0.1-svn333623-1~exp1~20180604222746.83 (branches/release_60)"}
