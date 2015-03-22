Title: Bad Google repository signatures
Date: 2015-03-22T03:50:57Z
Summary: Google's package repositories occasionally return inconsistent data, causing validation failures.

Google publishes [Linux software repositories] for several of their products,
including Google Chrome, which is available from the following apt source:

``` .boxed
deb http://dl.google.com/linux/chrome/deb/ stable main
```

These repositories are signed with an 8 year old 1024-bit DSA key:

``` .boxed
pub   1024D/7FAC5991 2007-03-08
      Key fingerprint = 4CCA 1EAF 950C EE4A B839  76DC A040 830F 7FAC 5991
uid                  Google, Inc. Linux Package Signing Key <linux-packages-keymaster@google.com>
sub   2048g/C07CB649 2007-03-08
```

Asymmetric 1024-bit keys are not considered strong enough and were, for
instance, [aggressively retired] from Google's SSL frontends almost two years
ago. Such short keys should not be used to protect the integrity of software
package repositories.

Note that this key has a longer 2048-bit ElGamal subkey, which is not actually
used to produce signatures, but only for encryption. In fact, only a signing key
is needed to sign the files in a secure apt repository, and, for instance, the
[archive keys] used to sign official debian.org repositories do not contain an
encryption subkey.

Since years, many users have reported an [error message] like the following when
running `apt-get update`:

``` .boxed
W: GPG error: http://dl.google.com stable Release: The following signatures were
invalid: BADSIG A040830F7FAC5991 Google, Inc. Linux Package Signing Key
<linux-packages-keymaster@google.com>
```

This error might resolve itself if `apt-get update` is run again. Apparently,
this is due to "[bad pushes]" occurring in the Google infrastructure. An example
of this can be seen in the following `curl` output:

``` .boxed
$ curl -v http://dl.google.com/linux/chrome/deb/dists/stable/Release \
        http://dl.google.com/linux/chrome/deb/dists/stable/Release.gpg
* Hostname was NOT found in DNS cache
*   Trying 74.125.196.136...
* Connected to dl.google.com (74.125.196.136) port 80 (#0)
> GET /linux/chrome/deb/dists/stable/Release HTTP/1.1
> User-Agent: curl/7.38.0
> Host: dl.google.com
> Accept: */*
> 
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Content-Length: 1347
< Content-Type: application/octet-stream
< Etag: "518b8"
< Expires: Sun, 22 Mar 2015 18:55:19 PDT
< Last-Modified: Fri, 20 Mar 2015 04:22:00 GMT
* Server downloads is not blacklisted
< Server: downloads
< X-Content-Type-Options: nosniff
< X-Frame-Options: SAMEORIGIN
< X-Xss-Protection: 1; mode=block
< Date: Sun, 22 Mar 2015 01:55:19 GMT
< Alternate-Protocol: 80:quic,p=0.5
< 
Origin: Google, Inc.
Label: Google
Suite: stable
Codename: stable
Version: 1.0
Date: Thu, 19 Mar 2015 22:55:29 +0000
Architectures: amd64 i386
Components: main
Description: Google chrome-linux repository.
MD5Sum:
 53375c7a2d182d85aef6218c179040ed 144 main/binary-i386/Release
 c556daf52ac818e4b11b84cb5943f6e0 4076 main/binary-i386/Packages
 867ba456bd6537e51bd344df212f4662 960 main/binary-i386/Packages.gz
 2b766b2639b57d5282a154cf6a00b172 1176 main/binary-i386/Packages.bz2
 89704f9af9e6ccd87c192de11ba4c511 145 main/binary-amd64/Release
 fa88101278271922ec9b14b030fd2423 4082 main/binary-amd64/Packages
 1ba717117027f36ff4aea9c3ea60de9e 962 main/binary-amd64/Packages.gz
 19af18f376c986d317cadb3394c60ac5 1193 main/binary-amd64/Packages.bz2
SHA1:
 59414c4175f2cc22e67ba6c30687b00c72a7eafc 144 main/binary-i386/Release
 1764c5418478b1077ada54c73eb501165ba79170 4076 main/binary-i386/Packages
 db24eafac51d3e63fd41343028fb3243f96cbed6 960 main/binary-i386/Packages.gz
 ad8be07425e88b2fdf2f6d143989cde1341a8c51 1176 main/binary-i386/Packages.bz2
 153199d8f866350b7853365a4adc95ee687603dd 145 main/binary-amd64/Release
 7ce66535b35d5fc267fe23af9947f9d27e88508b 4082 main/binary-amd64/Packages
 a72b5e46c3be8ad403df54e4cdcd6e58b2ede65a 962 main/binary-amd64/Packages.gz
 dbc7fddd28cc742ef8f0fb8c6e096455e18c35f8 1193 main/binary-amd64/Packages.bz2
* Connection #0 to host dl.google.com left intact
* Found bundle for host dl.google.com: 0x7f24e68d06a0
* Re-using existing connection! (#0) with host dl.google.com
* Connected to dl.google.com (74.125.196.136) port 80 (#0)
> GET /linux/chrome/deb/dists/stable/Release.gpg HTTP/1.1
> User-Agent: curl/7.38.0
> Host: dl.google.com
> Accept: */*
> 
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Content-Length: 198
< Content-Type: application/octet-stream
< Etag: "518f4"
< Expires: Sun, 22 Mar 2015 18:55:19 PDT
< Last-Modified: Fri, 20 Mar 2015 04:05:00 GMT
* Server downloads is not blacklisted
< Server: downloads
< X-Content-Type-Options: nosniff
< X-Frame-Options: SAMEORIGIN
< X-Xss-Protection: 1; mode=block
< Date: Sun, 22 Mar 2015 01:55:19 GMT
< Alternate-Protocol: 80:quic,p=0.5
< 
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.10 (GNU/Linux)

iEYEABECAAYFAlULm7YACgkQoECDD3+sWZFyxACeNPuK/zQ0v+3Py1n2s09Wk/Ti
DckAni8V/gy++xIinu8OdUXv7c777V9H
=5vT6
-----END PGP SIGNATURE-----
* Connection #0 to host dl.google.com left intact
```

Note that both the `Release` and `Release.gpg` files were fetched with the same
HTTP connection, so the two files must have come from the same web frontend.
(Though, it is possible they were served by different backends.) However, the
detached signature in `Release.gpg` does not match the content in `Release`:

``` .boxed
gpgv: Signature made Fri 20 Mar 2015 12:01:58 AM EDT using DSA key ID 7FAC5991
gpgv: BAD signature from "Google, Inc. Linux Package Signing Key <linux-packages-keymaster@google.com>"
```

Performing the same pair of fetches again, the same `Release.gpg` file is
returned, but the `Release` file is slightly different:

``` .boxed
$ curl -v http://dl.google.com/linux/chrome/deb/dists/stable/Release \
        http://dl.google.com/linux/chrome/deb/dists/stable/Release.gpg
* Hostname was NOT found in DNS cache
*   Trying 74.125.196.136...
* Connected to dl.google.com (74.125.196.136) port 80 (#0)
> GET /linux/chrome/deb/dists/stable/Release HTTP/1.1
> User-Agent: curl/7.38.0
> Host: dl.google.com
> Accept: */*
> 
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Content-Length: 1347
< Content-Type: application/octet-stream
< Etag: "518f3"
< Expires: Sun, 22 Mar 2015 18:55:04 PDT
< Last-Modified: Fri, 20 Mar 2015 04:05:00 GMT
* Server downloads is not blacklisted
< Server: downloads
< X-Content-Type-Options: nosniff
< X-Frame-Options: SAMEORIGIN
< X-Xss-Protection: 1; mode=block
< Date: Sun, 22 Mar 2015 01:55:04 GMT
< Alternate-Protocol: 80:quic,p=0.5
< 
Origin: Google, Inc.
Label: Google
Suite: stable
Codename: stable
Version: 1.0
Date: Fri, 20 Mar 2015 04:02:02 +0000
Architectures: amd64 i386
Components: main
Description: Google chrome-linux repository.
MD5Sum:
 89704f9af9e6ccd87c192de11ba4c511 145 main/binary-amd64/Release
 fa88101278271922ec9b14b030fd2423 4082 main/binary-amd64/Packages
 1ba717117027f36ff4aea9c3ea60de9e 962 main/binary-amd64/Packages.gz
 19af18f376c986d317cadb3394c60ac5 1193 main/binary-amd64/Packages.bz2
 53375c7a2d182d85aef6218c179040ed 144 main/binary-i386/Release
 c556daf52ac818e4b11b84cb5943f6e0 4076 main/binary-i386/Packages
 867ba456bd6537e51bd344df212f4662 960 main/binary-i386/Packages.gz
 2b766b2639b57d5282a154cf6a00b172 1176 main/binary-i386/Packages.bz2
SHA1:
 153199d8f866350b7853365a4adc95ee687603dd 145 main/binary-amd64/Release
 7ce66535b35d5fc267fe23af9947f9d27e88508b 4082 main/binary-amd64/Packages
 a72b5e46c3be8ad403df54e4cdcd6e58b2ede65a 962 main/binary-amd64/Packages.gz
 dbc7fddd28cc742ef8f0fb8c6e096455e18c35f8 1193 main/binary-amd64/Packages.bz2
 59414c4175f2cc22e67ba6c30687b00c72a7eafc 144 main/binary-i386/Release
 1764c5418478b1077ada54c73eb501165ba79170 4076 main/binary-i386/Packages
 db24eafac51d3e63fd41343028fb3243f96cbed6 960 main/binary-i386/Packages.gz
 ad8be07425e88b2fdf2f6d143989cde1341a8c51 1176 main/binary-i386/Packages.bz2
* Connection #0 to host dl.google.com left intact
* Found bundle for host dl.google.com: 0x7ffa33d8b6a0
* Re-using existing connection! (#0) with host dl.google.com
* Connected to dl.google.com (74.125.196.136) port 80 (#0)
> GET /linux/chrome/deb/dists/stable/Release.gpg HTTP/1.1
> User-Agent: curl/7.38.0
> Host: dl.google.com
> Accept: */*
> 
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Content-Length: 198
< Content-Type: application/octet-stream
< Etag: "518f4"
< Expires: Sun, 22 Mar 2015 18:55:05 PDT
< Last-Modified: Fri, 20 Mar 2015 04:05:00 GMT
* Server downloads is not blacklisted
< Server: downloads
< X-Content-Type-Options: nosniff
< X-Frame-Options: SAMEORIGIN
< X-Xss-Protection: 1; mode=block
< Date: Sun, 22 Mar 2015 01:55:05 GMT
< Alternate-Protocol: 80:quic,p=0.5
< 
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.10 (GNU/Linux)

iEYEABECAAYFAlULm7YACgkQoECDD3+sWZFyxACeNPuK/zQ0v+3Py1n2s09Wk/Ti
DckAni8V/gy++xIinu8OdUXv7c777V9H
=5vT6
-----END PGP SIGNATURE-----
* Connection #0 to host dl.google.com left intact
```

Note that the `Date` line in the `Release` file is different:

``` .boxed
@@ -6 +6 @@
-Date: Thu, 19 Mar 2015 22:55:29 +0000
+Date: Fri, 20 Mar 2015 04:02:02 +0000
```

The file hashes listed in the `Release` file are in a different order, as well,
though the actual hash values are the same. This `Release` file **does** have a
valid signature:

``` .boxed
gpgv: Signature made Fri 20 Mar 2015 12:01:58 AM EDT using DSA key ID 7FAC5991
gpgv: Good signature from "Google, Inc. Linux Package Signing Key <linux-packages-keymaster@google.com>"
```

Note that the `Release.gpg` files in the good and bad cases are the same, and
the same signature cannot cover two files with different content. Also note that
the same mis-signed content is [available via HTTPS], so it is probably not
caused by a MITM attack.

The possibility of skew between the `Release` and `Release.gpg` files is
precisely why [inline signed Release files] were introduced, but Google's
repositories use only the older format with a detached signature.

It would be nice if Google could fix the underlying bug in their infrastructure
that results in mis-signed repositories being published frequently, because it
trains users to ignore cryptographic failures.

[Linux software repositories]: https://www.google.com/linuxrepositories/
[aggressively retired]: http://googleonlinesecurity.blogspot.com/2013/11/out-with-old-stronger-certificates-with.html
[archive keys]: https://ftp-master.debian.org/keys.html
[error message]: https://www.google.com/search?q=%22BADSIG+A040830F7FAC5991%22
[bad pushes]: https://code.google.com/p/chromium/issues/detail?id=107334#c12
[available via HTTPS]: https://dl.google.com/linux/chrome/deb/dists/stable/Release
[inline signed Release files]: https://lists.debian.org/debian-devel-announce/2009/11/msg00001.html
