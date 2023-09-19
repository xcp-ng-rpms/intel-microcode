# Citrix does not publish SRPMs for their package, so we're duplicating efforts
%define xs_release 1
%define xs_dist xs8

Summary:        Intel Microcode
Name:           intel-microcode
Version:        20230720
Release:        %{xs_release}%{?dist}
License:        Redistributable, no modification permitted
URL:            https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/

# Source tarball created with `rpm2archive intel-microcode-%{version}-%{xs_release}-%{xs_dist}.noarch.rpm`
Source0:        %{name}-%{version}-%{xs_release}.%{xs_dist}.noarch.rpm.tgz

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
* Tue Sep 19 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 20230720-1
- Update to IPU 2023.3 release

* Fri Mar 17 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 20230206-1
- Update to IPU 2023.1 release

* Mon Dec 19 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 20221013-1
- Update to 20221013

* Wed Oct 05 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 20220504-1
- Create intel-microcode RPM
