from fastecdsa import curvemath


class Curve:
    """Representation of an elliptic curve.

    Supports the arithmetic operations of point addition and scalar multiplication. Currently only
    curves defined via the equation :math:`y^2 \equiv x^3 + ax + b \pmod{p}` are supported.

    Attributes:
        |  name (string): The name of the curve
        |  p (long): The value of :math:`p` in the curve equation.
        |  a (long): The value of :math:`a` in the curve equation.
        |  b (long): The value of :math:`a` in the curve equation.
        |  G (long, long): The base point of the curve.
        |  q (long): The order of the base point of the curve.
    """

    def __init__(self, name, p, a, b, q, gx, gy):
        """Initialize the parameters of an elliptic curve.

        WARNING: Do not generate your own parameters unless you know what you are doing or you could
        generate a curve severely less secure than you think. Even then, consider using a
        standardized curve for the sake of interoperability.

        Currently only curves defined via the equation :math:`y^2 \equiv x^3 + ax + b \pmod{p}` are
        supported.

        Args:
            |  name (string): The name of the curve
            |  p (long): The value of :math:`p` in the curve equation.
            |  a (long): The value of :math:`a` in the curve equation.
            |  b (long): The value of :math:`a` in the curve equation.
            |  q (long): The order of the base point of the curve.
            |  gx (long): The x coordinate of the base point of the curve.
            |  gy (long): The y coordinate of the base point of the curve.
        """
        self.name = name
        self.p = p
        self.a = a
        self.b = b
        self.G = (gx, gy)
        self.q = q

    def is_point_on_curve(self, P):
        """ Check if a point lies on this curve.

        The check is done by evaluating the curve equation :math:`y^2 \equiv x^3 + ax + b \pmod{p}`
        at the given point :math:`(x,y)` with this curve's domain parameters :math:`(a, b, p)`. If
        the congruence holds, then the point lies on this curve.

        Args:
            P (long, long): A tuple representing the point :math:`P` as an :math:`(x, y)` coordinate
            pair.

        Returns:
            bool: :code:`True` if the point lies on this curve, otherwise :code:`False`.
        """
        x, y, = P[0], P[1]
        left = y * y
        right = (x * x * x) + (self.a * x) + self.b
        return (left - right) % self.p == 0

    def point_mul(self, P, d):
        """Multiply a point on this curve by a scalar.

        First check if the point being multiplied actually lies on this curve. If it does then use
        Montgomery Point Multiplication to obtain the resulting point.

        Args:
            |  P (long, long): A tuple representing the point :math:`P` as an :math:`(x, y)`
              coordinate pair.
            |  d (long): An integer to multiply the point by.

        Returns:
            (long, long): A point on the curve if :math:`P` lies on the curve, otherwise
            :math:`(0,0)`.
        """
        if self.is_point_on_curve(P):
            x, y = curvemath.mul(str(P[0]), str(P[1]), str(d), self.name)
            return int(x), int(y)
        else:
            return (0, 0)

    def point_add(self, P, Q):
        """Add two points that are on this curve.

        First check if both points lie on the curve. If they do then add them using a Double-and-add
        method.

        Args:
            |  P (long, long): A tuple representing the point :math:`P` as an :math:`(x, y)`
               coordinate pair.
            |  Q (long, long): A tuple representing the point :math:`Q` as an :math:`(x, y)`
               coordinate pair.

        Returns:
            (long, long): A point on the curve if :math:`P` and :math:`Q` lie on the curve,
            otherwise :math:`(0,0)`.
        """
        if self.is_point_on_curve(P) and self.is_point_on_curve(Q):
            x, y = curvemath.add(str(P[0]), str(P[1]), str(Q[0]), str(Q[1]), self.name)
            return int(x), int(y)
        else:
            return (0, 0)


# see https://www.nsa.gov/ia/_files/nist-routines.pdf for params
P192 = Curve(
    'P192',
    6277101735386680763835789423207666416083908700390324961279,
    -3,
    2455155546008943817740293915197451784769108058161191238065,
    6277101735386680763835789423176059013767194773182842284081,
    602046282375688656758213480587526111916698976636884684818,
    174050332293622031404857552280219410364023488927386650641
)
P224 = Curve(
    'P224',
    26959946667150639794667015087019630673557916260026308143510066298881,
    -3,
    18958286285566608000408668544493926415504680968679321075787234672564,
    26959946667150639794667015087019625940457807714424391721682722368061,
    19277929113566293071110308034699488026831934219452440156649784352033,
    19926808758034470970197974370888749184205991990603949537637343198772
)
P256 = Curve(
    'P256',
    115792089210356248762697446949407573530086143415290314195533631308867097853951,
    -3,
    41058363725152142129326129780047268409114441015993725554835256314039467401291,
    115792089210356248762697446949407573529996955224135760342422259061068512044369,
    48439561293906451759052585252797914202762949526041747995844080717082404635286,
    36134250956749795798585127919587881956611106672985015071877198253568414405109
)
P384 = Curve(
    'P384',
    39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319,
    -3,
    27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575,
    39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643,
    26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087,
    8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871
)
P521 = Curve(
    'P521',
    6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151,
    -3,
    1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984,
    6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449,
    2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846,
    3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784
)

# see http://www.secg.org/sec2-v2.pdf for params
secp256k1 = Curve(
    'secp256k1',
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    0x0,
    0x7,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
)
