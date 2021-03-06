// REQUIRES: arm-registered-target
// RUN: %clang_cc1 -triple armv7 %s -emit-llvm -o /dev/null

char bar();

void t1(int x, char y) {
  __asm__ volatile("mcr p15, 0, %1, c9, c12, 5;"
                   "mrc p15, 0, %0, c9, c13, 2;"
                   : "=r" (x)
                   : "r" (bar())); // no warning
  __asm__ volatile("foo %0, %1"
                   : "+r" (x),
                     "+r" (y)
                   :);
}

// <rdar://problem/12284092>
typedef __attribute__((neon_vector_type(2))) long long int64x2_t;
typedef struct int64x2x4_t {
  int64x2_t val[4];
} int64x2x4_t;
int64x2x4_t t2(const long long a[]) {
  int64x2x4_t r;
  __asm__("vldm %[a], { %q[r0], %q[r1], %q[r2], %q[r3] }"
          : [r0] "=r"(r.val[0]), // expected-warning {{the value is truncated when put into register, use a modifier to specify the size}}
            [r1] "=r"(r.val[1]), // expected-warning {{the value is truncated when put into register, use a modifier to specify the size}}
            [r2] "=r"(r.val[2]), // expected-warning {{the value is truncated when put into register, use a modifier to specify the size}}
            [r3] "=r"(r.val[3])  // expected-warning {{the value is truncated when put into register, use a modifier to specify the size}}
          : [a] "r"(a));
  return r;
}
