class SensorDataLogger(context: Context) {
    private val dataFile: File = File(context.getExternalFilesDir(null), "gyro_data.csv")
    private val data = mutableListOf<SensorReading>()
    
    data class SensorReading(
        val timestamp: Long,
        val axisX: Float,
        val axisY: Float,
        val axisZ: Float,
        val label: String = "" // For labeled training data
    )
    
    fun logReading(event: SensorEvent, label: String = "") {
        data.add(SensorReading(
            timestamp = System.currentTimeMillis(),
            axisX = event.values[0],
            axisY = event.values[1],
            axisZ = event.values[2],
            label = label
        ))
    }
    
    fun saveToDisk() {
        dataFile.appendText(data.joinToString("\n") { reading ->
            "${reading.timestamp},${reading.axisX},${reading.axisY},${reading.axisZ},${reading.label}"
        })
        data.clear()
    }
}
