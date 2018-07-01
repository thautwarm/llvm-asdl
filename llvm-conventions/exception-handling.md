LLVM ABI: Exception Handling
=============================================

Type Info For Custom Structure
------------------------------------------------------------------

Firstly we link the following one for creating your new type info:

```llvm
@_ZTVN10__cxxabiv117__class_type_infoE = external global i8*
```

Next, for any type `S`, its type info is:

```llvm

@_ZTS{len(S)}{S} = linkonce_odr constant [ {(len(S) + 2)} x i8] c"{len(S)}{S}\00", comdat

@_ZTI{len(S)}{S} = linkonce_odr constant { i8*, i8* }
                        {
                            i8* bitcast (
                                    i8** getelementptr (i8*, i8** _ZTVN10__cxxabiv117__class_type_infoE, i64 2)
                                to i8*
                                ),

                            i8* getelementptr inbounds (
                                    [{(len(S) + 2)} x i8],
                                    [{(len(S) + 2)} x i8]*
                                    @_ZTS{len(S)}{S}, i32 0, i32 0)
                        }

```

In above snippet I use syntaxes like Jinja2 in a LLVM IR template. Once the name of your custom structrue `S` is decided,
replace the blocks like `{...}` in the template by evaluating them with a known variable `S`.

Exception Handling
--------------------------------------------

- Throw Exception

    For any exception you want to catch, you should use `@__cxa_allocate_exception`
    to allocate a piece of buffer of type `i8*` sized the same size of your exception.

    Here is an example:

    In the head of IR file:

    ```llvm
    %struct.Ex = type { i32 }  ; i32 takes 4 bytes.
    ```

    In the head of your exception emitting function:

    ```llvm
    ; first allocate your exception data
        %.exc_data.i8 = call i8* @__cxa_allocate_exception(i64 4) #5

    ; if your data is not basic types(int, float, and so on)
        tail call void
            @llvm.memcpy.p0i8.p0i8.i64(
                i8* %.exc_data.i8,
                i8* bitcast (%{S}* @_ZTI{len(S)}{S} to i8*),
                i64 {size of your structure S},
                i32 {max size of the members in your structure S},
                i1 false) ; the last argument means isVolatile
    ; elseif S is of basic type
        store {S} , {S}* bitcast (i8* %.exc_data.i8 to {S}*), align 16

    ; then you can make `throw-statement`:

        invoke void @__cxa_throw(
                i8* %.exc_data.i8 ,
                i8* bitcast (i8** @_ZTI{len(S)}{S} to i8*),
                i8* null)
                to label %.if_not_raise unwind label %.if_raise
    ```


- Catch Exception

    Firstly, any function that need to do error handling must have an attribute `personality i8* bitcast (i32 (...)* @__gxx_personality_v0 to i8*)`,
    for instance:

    ```llvm

    declare i32 @__gxx_personality_v0(...)
    define @exc_fn()  personality i8* bitcast (i32 (...)* @__gxx_personality_v0 to i8*) {
        # do exception-handling
    }
    ```


    The `try-statement` is trial, you should use `landingpad` instruction to implement it:

    ```llvm
        %.exc_pad = landingpad { i8*, i32 }
          catch i8* bitcast (i8** @_ZTI{len(S)}{S}to i8*)
          ; you can catch more than one exception types here! :-)
          ; you can use `filter [n x i8**] [exctyp1, ..., exctypn]` here to 
          ;   do filtering for some unexpected exceptions are inherited from others.

        %.exc.typeid = extractvalue { i8*, i32 } %.exc_pad, 1
        %.exc.typeid.expected = tail call i32 @llvm.eh.typeid.for(i8* bitcast (i8** @_ZTIi to i8*))
        %.exc.typeid.tested = icmp eq i32 %.exc.typeid, %.exc.typeid.expected
        br i1 %.exc.typeid.tested, label %.if_matched, label %.if_not_matched

    .if_matched:
        %.exc_type_info = extractvalue { i8*, i32 } %.exc_pad, 0
        tail call i8* @__cxa_begin_catch(i8* %.exc_type_info)
        # do some stuff when catching matched.
        tail call void @__cxa_end_catch()

    .if_not_matched:
        resume { i8*, i32 } %.exc_pad

    .exc.unreachable:
        unreachable
    ```
    where `S` is the name of your exception structure type.



