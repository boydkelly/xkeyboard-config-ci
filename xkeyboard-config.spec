# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%global debug_package %{nil}

# Installed destination is now xkeyboard-config-2, but upstream package
# name is the same
%global pkgconfig_name xkeyboard-config-2

Summary:    X Keyboard Extension configuration data
Name:       xkeyboard-config
Version:    2.48
Release:    13%{?dist}
License:    HPND AND HPND-sell-variant AND X11 AND X11-distribute-modifications-variant AND MIT AND MIT-open-group AND xkeyboard-config-Zinoviev
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig

Source0:    https://xorg.freedesktop.org/archive/individual/data/%{name}/%{name}-%{version}.tar.xz
Patch01:    0001-f45-ci.patch

BuildArch:  noarch

BuildRequires:  gettext gettext-devel
BuildRequires:  meson
BuildRequires:  libxslt
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(x11) >= 1.4.3
BuildRequires:  pkgconfig(xorg-macros) >= 1.12
BuildRequires:  pkgconfig(xproto) >= 7.0.20
BuildRequires:  xkbcomp
BuildRequires:  git-core

%description
This package contains configuration data used by the X Keyboard Extension (XKB),
which allows selection of keyboard layouts when using a graphical interface.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
Development files for %{name}.

%prep
%autosetup -S git

%build
%meson -Dcompat-rules=true -Dxorg-rules-symlinks=true
%meson_build

%install
%meson_install

# Replace with relative symlink
rm $RPM_BUILD_ROOT%{_datadir}/X11/xkb
ln -srf $RPM_BUILD_ROOT%{_datadir}/%{pkgconfig_name} $RPM_BUILD_ROOT%{_datadir}/X11/xkb

%find_lang %{pkgconfig_name}
%find_lang %{name}

%pretrans -p <lua>
-- Define the path to directory being replaced below.
-- DO NOT add a trailing slash at the end.
local path = "%{_datadir}/X11/xkb"
local st = posix.stat(path)

if st and st.type == "directory" then
  local target = path .. ".rpmmoved"
  local suffix = 1

  while posix.stat(target) do
    suffix = suffix + 1
    target = path .. ".rpmmoved" .. suffix
  end

  os.rename(path, target)
end

%files -f %{pkgconfig_name}.lang -f %{name}.lang
%license COPYING
%doc AUTHORS README.md COPYING docs/README.* docs/HOWTO.*
%{_mandir}/man7/%{name}.*
%{_mandir}/man7/%{pkgconfig_name}.*
%{_datadir}/X11/xkb
%{_datadir}/%{pkgconfig_name}/
%ghost %attr(0755, root, root) %dir %{_datadir}/X11/xkb.rpmmoved

%files devel
%{_datadir}/pkgconfig/%{pkgconfig_name}.pc
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Fri Aug 07 2026 Boyd Kelly <bkelly@coastsystems.net> - 2.48-13
- xkeyboard-config 2.48
  Rebuilt with syntax fixes in custom ci (Côte d'Ivoire) layouts (corrected AE09 and AD11 keys)

* Sun Aug 02 2026 Boyd Kelly <bkelly@coastsystems.net> - 2.48-12
- xkeyboard-config 2.48
  Rebuilt with updated ci (Côte d'Ivoire) layouts; Release 12 (updated AE02/AE07 and visually improved syntax)

* Sun Aug 02 2026 Boyd Kelly <bkelly@coastsystems.net> - 2.48-11
- xkeyboard-config 2.48
  Rebuilt with corrected patch mapping updated layouts (resolved AE02 & AE07 values)

* Sun Aug 02 2026 Boyd Kelly <bkelly@coastsystems.net> - 2.48-10
- xkeyboard-config 2.48
  Rebuilt with updated ci (Côte d'Ivoire) layouts; Release 6
