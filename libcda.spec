Name: libcda
Version: 0.5
Release: 1
Source: http://tjaden.strangesoft.net/libcda/%name-%version.tar.gz
Summary: Minimalistic library for playing Audio CDs
URL: http://libcda.sf.net/
License: BSD
Group: System/Libraries

%track
prog %name = {
	url = http://tjaden.strangesoft.net/libcda/
	regex = "version (__VER__)"
	version = %version
}

%description
Minimalistic library for playing Audio CDs

%package devel
Summary: Development files for %name
Group: Development/C
Requires: %name = %version-%release

%description devel
Development files (Headers etc.) for %name.

%package static-devel
Summary: Static libraries for linking to %name
Group: Development/C
Requires: %name-devel = %version-%release

%description static-devel
Static libraries for linking to %name.

Install this package if you wish to develop or compile applications using
%name statically (users of the resulting binary won't need %name installed
with static linking).

%prep
%setup -q

%build
# Included Makefile can't crosscompile and builds only a static lib
%__cc $RPM_OPT_FLAGS -fPIC -DPIC -o linux.o -c linux.c
%__cc $RPM_OPT_FLAGS -g -shared -Wl,-soname=%{name}.so.0 -o %{name}.so.0 linux.o
if false; then
	# Actually if crosscompiling
	%_target_platform-ar cru %name.a linux.o
	%_target_platform-ranlib %name.a
else
	ar cru %name.a linux.o
	ranlib %name.a
fi

%install
mkdir -p $RPM_BUILD_ROOT%_libdir $RPM_BUILD_ROOT%_includedir/%name
install -c -m 755 %name.so.0 $RPM_BUILD_ROOT%_libdir/
install -c -m 644 %name.a $RPM_BUILD_ROOT%_libdir/
install -c -m 644 libcda.h $RPM_BUILD_ROOT%_includedir/%name/
ln -s %name.so.0 $RPM_BUILD_ROOT%_libdir/%name.so

%files
%_libdir/*.so*

%files devel
%_includedir/*

%files static-devel
%_libdir/*.a

%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/%name-%version
