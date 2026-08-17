import android.content.Context
import android.hardware.SensorEvent
import java.io.File

class SensorDataLogger(context: Context) {
    private val gyroFile: File = File(context.getExternalFilesDir(null), "gyro_data.csv")
    private val framesFile: File = File(context.getExternalFilesDir(null), "frames.csv")

    private val gyroBuffer = mutableListOf<SensorReading>()
    private val frameList = mutableListOf<FrameRecord>()

    data class SensorReading(
        val timestampNanos: Long, // monotonic nanoseconds (SensorEvent.timestamp)
        val axisX: Float,
        val axisY: Float,
        val axisZ: Float,
        val label: String = ""
    )

    data class FrameRecord(
        val timestampNanos: Long, // monotonic nanoseconds (Image.getTimestamp() or CaptureResult.SENSOR_TIMESTAMP)
        val filename: String
    )

    // Log sensor reading using SensorEvent.timestamp (nanos)
    fun logReading(event: SensorEvent, label: String = "") {
        gyroBuffer.add(SensorReading(
            timestampNanos = event.timestamp,
            axisX = event.values[0],
            axisY = event.values[1],
            axisZ = event.values[2],
            label = label
        ))
    }

    // When a frame is captured, call this with the frame timestamp and the saved filename
    fun recordFrame(timestampNanos: Long, filename: String) {
        frameList.add(FrameRecord(timestampNanos, filename))
    }

    // Persist both CSVs. Timestamp is in nanoseconds (monotonic).
    fun saveToDisk() {
        if (gyroBuffer.isNotEmpty()) {
            gyroFile.appendText(gyroBuffer.joinToString("\n") { r ->
                "${r.timestampNanos},${r.axisX},${r.axisY},${r.axisZ},${r.label}"
            } + "\n")
            gyroBuffer.clear()
        }
        if (frameList.isNotEmpty()) {
            framesFile.appendText(frameList.joinToString("\n") { f ->
                "${f.timestampNanos},${f.filename}"
            } + "\n")
            frameList.clear()
        }
    }
}