
#include "nga_vm.hpp"

#include "..\..\build\depends\argparse\argparse.h"

bool weirdEquals(const std::wstring& str, char const* c)
{
  std::string c_str(c);
  if (str.size() < c_str.size())
  {
    return false;
  }
  return std::equal(c_str.begin(), c_str.end(), str.begin());
}

extern int64_t ngaImageCells;
extern int64_t ngaImage[];

#ifndef BIT64
#define CELL int32_t
#define CELL_MIN INT_MIN + 1
#define CELL_MAX INT_MAX - 1
#else
#define CELL int64_t
#define CELL_MIN LLONG_MIN + 1
#define CELL_MAX LLONG_MAX - 1
#endif

#define IMAGE_SIZE   1000000       /* Amount of RAM. 968kB by default.  */
#define ADDRESSES    256          /* Depth of address stack            */
#define STACK_DEPTH  128          /* Depth of data stack               */

using namespace argparse;

extern "C" {
  int wmain_sqlite(int argc, wchar_t** wargv);
};

char* argv[64];
char argv_heap[4097];
int argv_next = 0;

int wmain(int argc, wchar_t** wargv) {

  for (int i = 0; i < argc; i++) {
    std::wstring arg(wargv[i]);
    argv[i] = &argv_heap[argv_next];
    for (size_t iter = 0; iter < arg.length(); iter++) {
      argv_heap[argv_next++] = (char)arg[i];
    }
    argv_heap[argv_next++] = 0;
  }

  ArgumentParser parser("./retro.exe", "Argument parser example");

  parser.add_argument()
    .names({ "-s", "--sqlite" })
    .description("sqlite shell")
    .required(false);

  //parser.add_argument("-t", "--test", "test")
  //  .position(ArgumentParser::Argument::Position::LAST);

  //parser.add_argument("-d", "--dtest", "dtest").position(0);

  parser.enable_help();


  auto err = parser.parse(argc, (const char**)argv);
  if (err) {
    std::cout << err << std::endl;
    return -1;
  }

  if (parser.exists("help")) {
    parser.print_help();
    return 0;
  }

  //auto vm = RETRO_VM<CELL, IMAGE_SIZE, STACK_DEPTH, ADDRESSES>(CELL_MIN, CELL_MAX);
  //vm.ngaLoadImage("ngaImage", ngaImage, ngaImageCells);
  //vm.execute(0);

  if (parser.exists("s")) {
    wchar_t sqlite_wargv[32];
    return wmain_sqlite(0, (wchar_t**)&sqlite_wargv);


    /*
    switch (parser.get<unsigned int>("v")) {
    case 2:
      std::cout << "an even more verbose string" << std::endl;
#ifdef __clang__
      [[clang::fallthrough]];
#endif
      // fall through
    case 1:
      std::cout << "a verbose string" << std::endl;
#ifdef __clang__
      [[clang::fallthrough]];
#endif
      // fall through
    default:
      std::cout << "some verbosity" << std::endl;
    }
    */
  }

  if (parser.exists("test")) {
    std::cout << parser.get<std::string>("test") << std::endl;
  }

  if (parser.exists("dtest")) {
    std::cout << parser.get<std::string>("dtest") << std::endl;
  }

  exit(0);
}
