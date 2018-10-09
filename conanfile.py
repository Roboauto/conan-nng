#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class NngConan(ConanFile):
    name = "nng"
    version = "1.0.1"
    url="https://github.com/gavinNL/conan-nng"
    description = "a socket library that provides several common communication patterns"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    generators = "cmake"
    source_subfolder = "source_subfolder"
    options = {
        "shared": [True, False],
       "enable_tests": [True, False],
       "enable_tools": [True, False],
       "enable_nngcat": [True, False],
    }

    default_options = (
        "shared=False",
        "enable_tests=False",
        "enable_tools=False",
        "enable_nngcat=False"
    )

    def source(self):
        source_url = "https://github.com/nanomsg/nng"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        cmake = CMake(self)
        cmake.definitions["NNG_TESTS"] = self.options.enable_tests
        cmake.definitions["NNG_ENABLE_TOOLS"] = self.options.enable_tools
        cmake.definitions["NNG_ENABLE_NNGCAT"] = self.options.enable_nngcat
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        self.copy("*.h", dst="include", src="install/include")
        self.copy("*.dll", dst="bin", src="install/bin")
        self.copy("*.lib", dst="lib", src="install/lib")
        self.copy("*.a", dst="lib", src="install/lib")
        self.copy("*.so*", dst="lib", src="install/lib")
        self.copy("*.dylib", dst="lib", src="install/lib")
        self.copy("nngcat*", dst="bin", src="install/bin")
        self.copy("*.*", dst="lib/pkgconfig", src="install/lib/pkgconfig")

    def package_info(self):
        self.cpp_info.libs = ["nng"]

        if self.settings.os == "Windows":
            if not self.options.shared:
                self.cpp_info.libs.append('mswsock')
                self.cpp_info.libs.append('ws2_32')
        elif self.settings.os == "Linux":
            #self.cpp_info.libs.append('anl')
            self.cpp_info.libs.append('pthread')
            pass
