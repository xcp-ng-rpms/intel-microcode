# Citrix does not publish SRPMs for their package, so we're duplicating efforts
%define xs_release 1
%define xs_dist xs8

Summary:        Intel Microcode
Name:           intel-microcode
# This is the version coming from XenServer, who gets the microcode in advance
# so they have a different date from the public release.
# Put the public release version in the changelog when applicable.
Version:        20250501
Release:        %{xs_release}%{?dist}
License:        Redistributable, no modification permitted
URL:            https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/

# Source tarball created with `rpm2archive intel-microcode-%{version}-%{xs_release}-%{xs_dist}.noarch.rpm`
Source0:        %{name}-%{version}-%{xs_release}.%{xs_dist}.noarch.rpm.tgz

# XCP-ng: Dropped by Intel in their updates, relates early steppings of
# Sapphire Rapids, we keep them in case some homelabber got their hands on
# these, but they won't be updated.
Source1: 06-8f-05
Source2: 06-8f-06

BuildArch:      noarch
BuildRequires:  kernel-devel

%description
Microcode blobs for Intel CPUs.

%prep
%setup -q -c

%build

%install
mkdir -p %{buildroot}/lib/firmware/intel-ucode
install -m 644 lib/firmware/intel-ucode/* %{buildroot}/lib/firmware/intel-ucode
# The files that we provide directly in SOURCES must not exist in the archive
# If the following fails, then we must review what we do with these extra ucode files
[ ! -f "%{buildroot}/lib/firmware/intel-ucode/$(basename %SOURCE1)" ] || exit 1
[ ! -f "%{buildroot}/lib/firmware/intel-ucode/$(basename $SOURCE2)" ] || exit 1
install -m 644 %{SOURCE1} %{buildroot}/lib/firmware/intel-ucode
install -m 644 %{SOURCE2} %{buildroot}/lib/firmware/intel-ucode

%check
# XS gets `06-4f-01` from Intel's intel-ucode-with-caveats directory.
# Were we to use Intel's tarball directly as source for this RPM, we'd risk
# forgetting about it.
# Hence this security to remember to adapt the packaging if/when we do so.
# (we could do it by simply listing the file in %%files, but it would then get listed twice)
if [ ! -f %{buildroot}/lib/firmware/intel-ucode/06-4f-01 ]; then
    echo "Missing 06-4f-01! Genuine removal, or packaging needs adapting?"
    exit 1
fi

%post
%{regenerate_initrd_post}

%postun
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%clean
rm -rf %{buildroot}

%files
%license usr/share/licenses/%{name}-%{version}/*
%doc usr/share/doc/%{name}-%{version}/*
/lib/firmware/intel-ucode

%changelog
* Mon May 12 2025 Samuel Verschelde <stormi-xcp@ylix.fr> - 20250501-1
- Update to publicly released microcode-20250512
- Security updates for:
    - INTEL-SA-01153
    - INTEL-SA-01244
    - INTEL-SA-01247
    - INTEL-SA-01322
- Updates for multiple functional issues
- Upstream doesn't provide updates for older Sapphire Rapids steppings, we kept the last known versions

* Fri Feb 21 2025 David Morel <david.morel@vates.tech> - 20250127-1
- Update to publicly released microcode-20250211
- Security updates for:
    - INTEL-SA-01166
    - INTEL-SA-01213
    - INTEL-SA-01139
    - INTEL-SA-01228
- Updates for multiple functional issues
- Upstream update drops files for older Sapphire Rapids steppings, we kept the previous versions

* Wed Nov 13 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20241016-1
- Update to publicly released microcode-20241112

* Wed Oct 02 2024 David Morel <david.morel@vates.tech> - 20240815-1
- Update to latest version of IPU 2024.3

* Tue Aug 27 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20240717-1
- Update to IPU 2024.3 release
- As the archive from XS is missing an update for 06-a5-03 due to Intel
  initially forgetting to release its update, we manually package this file.

* Wed Jun 19 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20240419-1
- Update to IPU 2024.2 release

* Fri Apr 12 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20240130-1
- Update to IPU 2024.1 release

* Tue Jan 23 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 20231009-1
- Update to IPU 2023.4 release

* Tue Sep 19 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 20230720-1
- Update to IPU 2023.3 release

* Fri Mar 17 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 20230206-1
- Update to IPU 2023.1 release

* Mon Dec 19 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 20221013-1
- Update to 20221013

* Wed Oct 05 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 20220504-1
- Create intel-microcode RPM
