#include <idc.idc>

static decrypt(start,end)
{
  auto i;
  auto length = end - start;
  for ( i=0; i < length; i=i+1 )
  {
    auto b = get_wide_byte(start);
    b = b ^ 0x49 ^ (start >> 8);
    patch_byte(start, b);
    start = start + 1;
  }
}

static decrypt(void)
{
  memcpy(0x500, 0x500+0x7B00);
}
