

import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import org.tensorflow.contrib.android.TensorFlowInferenceInterface;


public class NeuralNetwork implements IDisposable {

	protected static final String MODEL_ASSET_PATH = "model.pb";
	protected static final String INPUT_TENSOR_NAME = "input:0";
	protected static final String OUTPUT_TENSOR_NAME = "output:0";
	public static final int PRED_NUM = 7;
	public static final int INPUT_SIZE = 12*20;

	TensorFlowInferenceInterface tf;
	float[] output = new float[PRED_NUM]; //['straight', 'left', 'right', 'stairs up', 'stairs down', 'normal', 'problem']

	public NeuralNetwork(AppCompatActivity act) {
		tf = new TensorFlowInferenceInterface(act.getAssets(), MODEL_ASSET_PATH);
	}

	public void dispose() {
		if (tf != null) tf.close();
		tf = null;
	}

	public float[] process(float[] input) {
		if(!initialized )
			return null;
		try {
			//Call tensorflow
			tf.feed(INPUT_TENSOR_NAME, input, (long) INPUT_SIZE);
			tf.run(new String[]{OUTPUT_TENSOR_NAME});
			tf.fetch(OUTPUT_TENSOR_NAME, output);
			return output;
		}
		catch (Exception e) {
			Log.e("tensorflow", "Couldn't run the tensorflow graph ("+e.toString()+")");
			checkCancel(bmp, true);
			return null;
		}
	}

	public bool addData(String name, float x, float y, float z) {
		/*
names = ['174630000602/Meas/Acc/13', '174630000602/Meas/Gyro/13', '174430000262/Meas/Acc/13', '174430000262/Meas/Gyro/13'],
generator => yield: name, time, x, y, z 
def combine(generator, names, file):
    try:
        data = []
        pos = {n:i for i, n in enumerate(names)}
        num = 0.0
        post = [None for _ in names]
        times = 0
        for name, time, x, y, z in generator():
            num += 1
            times += time
            post[pos[name]] = [x, y, z]
            fin = True
            for p in post:
                if p is None:
                    fin = False
                    break
            if fin:
                line = [times/num]
                times = 0
                num = 0
                for p in post:
                    for o in p:
                        line.append(o)
                post = [None for _ in names]
                data.append(line)
        with open(file, 'w') as f:
            f.write('time,'+','.join(n+'/x,'+n+'/y,'+n+'/z,' for n in names)+'\n')
            for d in data:
                f.write(','.join(map(str, d))+'\n')
    except:
		pass
	

smooth = data_smooth(data)
start = get_next_step(smooth, 0)
stop = get_next_step(smooth, start)
while start > 0 and stop > 0:
	data_all.append((data[start-1:stop+1], label))
	start = stop
	stop = get_next_step(smooth, start)

def get_next_step(smooth, start):
    """
        Find the next footstep
    """
    start = max(start+2, 3)
    for i in range(start, len(smooth)-9):
        grt = True
        for j in range(-3, 8):
            if smooth[i] < smooth[i+j]:
                grt = False
                break
        if grt:
            return i
	return -1
	

def data_abs(data):
    abs = np.abs(data[:, 0])
    for i in range(0, min(4, data.shape[1])):
        abs += np.abs(data[:, i])
    return abs

def data_smooth(data):
    abs = data_abs(data)
    smooth = abs[0:-6]+abs[1:-5]*2+abs[2:-4]*4+abs[3:-3]*4+abs[4:-2]*2+abs[5:-1]
    smooth = np.concatenate(([0,0,0], smooth, [0,0,0]))
    return smooth


		*/
		return false; //A step beginning and end found?
	}
}
