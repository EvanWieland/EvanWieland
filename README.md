<div id="header" align="center">
  <img src="https://raw.githubusercontent.com/EvanWieland/EvanWieland/5e5c695ebd8d042543acce2fdaed9e7c59df4ba1/assets/profile.jpg" width="200">
  <div id="badges">
    <br>
    <a href="https://www.linkedin.com/in/evan-w/">
      <img src="https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
    </a>
  </div>
  <div id="contact">
    <br>
    <a href="mailto:evan@bitsmithy.io">
      evan@bitsmithy.io
    </a>
  </div>
</div>

---

### 🏗️ Current Pet Project

<p align="center">
<img width="300" src="https://github.com/EvanWieland/Pudl/blob/master/brand/pudl-logo-light.png?raw=true">
</p>

Pudl is a simple, lightweight, and easily customizable programming language. [Go check it out!](https://github.com/EvanWieland/Pudl)

### About Pudl

Pudl is written using [LLVM](http://llvm.org/), the amazing compiler project. I've built this project off of the
great work done by [Max Balushkin](https://github.com/NoxChimaera). His approach to building a language without
relying on a third party parser/lexer combo - such as Bison/Flex, ANTLR, etc. - intrigued me. Although, I'm changing a
lot of the code to fit my needs, Balushkin's work still gave Pudl a huge jump start.

Expect more changes to Pudl in the future. This project is entirely for fun, so progress may be slow.

### Example

##### Pudl source code

```pudl
func inc( int a ) : int return a + 1

func mast : int {
  print inc( 5 )
  return 0
}
```

##### LLVM IR output (after optimization passes)

```llvm
; ModuleID = 'pudl compiler'
source_filename = "pudl compiler"

@.formati = private constant [4 x i8] c"%d\0A\00"
@.formatf = private constant [4 x i8] c"%f\0A\00"

declare i32 @printf(i8* %0, ...)

define i32 @inc(i32 %a) {
entry:
  %0 = add i32 %a, 1
  ret i32 %0
}

define i32 @mast() {
entry:
  %0 = call i32 @inc(i32 5)
  %1 = call i32 (i8*, ...) @printf(i8* noundef nonnull dereferenceable(1) getelementptr inbounds ([4 x i8], [4 x i8]* @.formati, i64 0, i64 0), i32 %0)
  ret i32 0
}
```

Go check [Pudl](https://github.com/EvanWieland/Pudl) out!

---


### 🔥 My Activity

[![GitHub Streak](https://github-readme-streak-stats.herokuapp.com?user=EvanWieland&theme=dark&date_format=M%20j%5B%2C%20Y%5D&background=000000)](https://github.com/EvanWieland)

[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=evanwieland&layout=compact&theme=vision-friendly-dark)](https://github.com/EvanWieland)
