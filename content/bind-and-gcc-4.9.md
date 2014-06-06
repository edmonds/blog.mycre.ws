Title: BIND and GCC 4.9
Date: 2014-06-06T02:19:08Z
Summary: ISC recommends compiling BIND with -fno-delete-null-pointer-checks on GCC 4.9.

ISC has issued an [operational notification] advising the use of the
`-fno-delete-null-pointer-checks` flag when compiling current versions of BIND
with GCC 4.9:

> Beginning with GCC 4.9.0, code optimization in GCC now includes (by default)
> an optimization which is intended to eliminate unnecessary null pointer
> comparisons in compiled code.  Unfortunately this optimization removes checks
> which are necessary in BIND and the demonstrated effect is to cause
> unpredictable assertion failures during execution of named, resulting in
> termination of the server process.
>
> Future versions of BIND will be modified so that the optimizer does not
> incorrectly remove necessary checks when building from source, and until those
> versions are available multiple immediate workarounds are available.

According to the [GCC documentation], `-fdelete-null-pointer-checks` performs
the following optimization, and is enabled by default even when compiling with
`-O0`:

> Assume that programs cannot safely dereference null pointers, and that no code
> or data element resides there. This enables simple constant folding
> optimizations at all optimization levels. In addition, other optimization
> passes in GCC use this flag to control global dataflow analyses that eliminate
> useless checks for null pointers; these assume that if a pointer is checked
> after it has already been dereferenced, it cannot be null.

This optimization [dates back to 1999] but it recently [became more aggressive]
in the GCC 4.9 release:

> GCC might now optimize away the null pointer check in code like:
>
>     int copy (int* dest, int* src, size_t nbytes) {
>       memmove (dest, src, nbytes);
>       if (src != NULL)
>         return *src;
>       return 0;
>     }
>
> The pointers passed to `memmove` (and similar functions in `<string.h>`) must
> be non-null even when `nbytes==0`, so GCC can use that information to remove
> the check after the `memmove` call. Calling `copy(p, NULL, 0)` can therefore
> deference a null pointer and crash.
>
> The example above needs to be fixed to avoid the invalid `memmove` call, for
> example:
>
>     if (nbytes != 0)
>       memmove (dest, src, nbytes);

It's interesting that the ISC operational advisory labels this an "incorrect"
optimization. I wonder if this is a similar case to the [Glibc optimization]
which exposed incorrect usage of `memcpy()` in many applications, [including
BIND].

Fortunately, few users should be affected by this bug, since GCC 4.9 is fairly
new. (The upcoming [Fedora 21 release] will probably be the first mainstream
distribution to ship with GCC 4.9 as the default compiler.)

[operational notification]: https://kb.isc.org/article/AA-01167
[GCC documentation]:        https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
[dates back to 1999]:       http://www.gnu.org/software/gcc/news/null.html
[became more aggressive]:   https://gcc.gnu.org/gcc-4.9/porting_to.html
[Glibc optimization]:       http://lwn.net/Articles/414467/
[including bind]:           https://kb.isc.org/article/AA-01085
[Fedora 21 release]:        http://fedoraproject.org/wiki/Releases/21/ChangeSet#GCC49
