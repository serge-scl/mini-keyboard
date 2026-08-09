class ARActivity : Activity(), SensorEventListener {
    private lateinit var sensorManager: SensorManager
    private var gyroscope: Sensor? = null
    private lateinit var dataLogger: SensorDataLogger

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        dataLogger = SensorDataLogger(this)
    }

    override fun onSensorChanged(event: SensorEvent) {
        if (event.sensor.type == Sensor.TYPE_GYROSCOPE) {
            // Log with optional label (e.g., "head_tilt_left", "idle")
            dataLogger.logReading(event, getCurrentGestureLabel())
        }
    }

    override fun onPause() {
        super.onPause()
        sensorManager.unregisterListener(this)
        dataLogger.saveToDisk() // Flush to disk
    }
}
