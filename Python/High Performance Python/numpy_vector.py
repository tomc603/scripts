import datetime
import sys
import numpy as np

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3


def show(output):
    """Convert list to numpy array, show using PIL"""
    try:
        import Image
        # convert our output to PIL-compatible input
        #import array
        #output = ((o + (256*o) + (256**2)*o) * 8 for o in output)
        #output = array.array('I', output)
        # display with PIL
        output = (output + (256*output) + (256**2)*output) * 8
        im = Image.new("RGB", (w/2, h/2))
        im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
        im.show()
    except ImportError as err:
        # Bail gracefully if we don't have PIL
        print "Couldn't import Image or numpy:", str(err)


def calculate_z_numpy(q, maxiter, z):
    """use vector operations to update all zs and qs to create new output array"""
    output = np.resize(np.array(0, dtype=np.int32), q.shape)
    for iteration in range(maxiter):
        z = z*z + q
        done = np.greater(abs(z), 2.0)
        q = np.where(done, 0+0j, q)
        z = np.where(done, 0+0j, z)
        output = np.where(done, iteration, output)
    return output


def calculate(show_output):
    # make a list of x and y values which will represent q
    # xx and yy are the co-ordinates, for the default configuration they'll look like:
    # if we have a 1000x1000 plot
    # xx = [-2.13, -2.1242, -2.1184000000000003, ..., 0.7526000000000064, 0.7584000000000064, 0.7642000000000064]
    # yy = [1.3, 1.2948, 1.2895999999999999, ..., -1.2844000000000058, -1.2896000000000059, -1.294800000000006]
    x_step = (float(x2 - x1) / float(w)) * 2
    y_step = (float(y1 - y2) / float(h)) * 2
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    x = np.array(x)
    y = np.array(y) * 1j # make y a complex number
    print "x and y have length:", len(x), len(y)

    # create a square matrix using clever addressing
    x_y_square_matrix = x+y[:, np.newaxis] # it is np.complex128
    # convert square matrix to a flatted vector using ravel
    q = np.ravel(x_y_square_matrix)
    # create z as a 0+0j array of the same length as q
    # note that it defaults to reals (float64) unless told otherwise
    z = np.zeros(q.shape, np.complex128)

    start_time = datetime.datetime.now()
    print "Total elements:", len(q)
    output = calculate_z_numpy(q, maxiter, z)
    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print "Main took", secs

    validation_sum = sum(output)
    print "Total sum of elements (for validation):", validation_sum

    if show_output:
        show(output)

    return validation_sum


if __name__ == "__main__":
    # get width, height and max iterations from cmd line
    # 'python mandelbrot_pypy.py 1000 1000'
    if len(sys.argv) == 1:
        w = h = 1000
        maxiter = 1000
    else:
        w = int(sys.argv[1])
        h = int(sys.argv[1])
        maxiter = int(sys.argv[2])

    # we can show_output for Python, not for PyPy
    validation_sum = calculate(True)

    # confirm validation output for our known test case
    # we do this because we've seen some odd behaviour due to subtle student
    # bugs
    if w == 1000 and h == 1000 and maxiter == 1000:
        assert validation_sum == 1148485 # if False then we have a bug

