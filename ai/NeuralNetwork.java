

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
}
