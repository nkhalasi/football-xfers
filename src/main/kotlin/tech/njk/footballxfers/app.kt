package tech.njk.footballxfers

import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import java.nio.file.Path
import java.nio.file.Paths

fun Double.format(digits: Int): String = java.lang.String.format("%.${digits}f", this)

data class Player(
    val href: String,
    val name: String,
    val position: String,
    val age: Int,
    val image: String,
    val nationality: String
)

data class Team(
    val href: String,
    val name: String,
    val country: String,
    val countryImage: String,
    val league: String,
    val leagueHref: String,
    val image: String
)

data class Transfer(
    val href: String,
    private val value: String,
    val timestamp: Long
) {
    val xferValue: Double get() =
        value.trim().let { originalAmtString ->
            val amtValString = if (originalAmtString == "?" || originalAmtString == "-" || originalAmtString == "" || originalAmtString == "0" || originalAmtString == "draft") "0" else originalAmtString.slice(IntRange(1, originalAmtString.length-1))
            when (amtValString.last().toString().toLowerCase()) {
                "m" -> amtValString.slice(IntRange(0, amtValString.length-2)).toDouble() * 1000 * 1000
                "k" -> amtValString.slice(IntRange(0, amtValString.length-2)).toDouble() * 1000
                else -> amtValString.toDouble()
            }
        }

}

data class GameSeason(
    val season: String,
    val player: Player,
    val from: Team,
    val to: Team,
    val transfer: Transfer
)

fun loadData(dataFile: Path): List<GameSeason> = dataFile.toFile().let {
    val mapper = jacksonObjectMapper()
    it.readLines().map { xferDataLine ->
        mapper.readValue<GameSeason>(xferDataLine)
    }
}

fun List<GameSeason>.top10Transfers() = this@top10Transfers.sortedBy { it.transfer.xferValue }.reversed().take(10)

private fun List<GameSeason>.teamWithMaxTransfers(filterFn: (GameSeason) -> Boolean, sortKeyFn: (GameSeason) -> String) =
    this@teamWithMaxTransfers.filter { filterFn(it) }
        .sortedBy(sortKeyFn)
        .groupBy(sortKeyFn)
        .map {
            Pair(it.key, it.value.size)
        }
        .sortedBy {
            it.second
        }
        .reversed()[0]

fun List<GameSeason>.teamWithMaxTransfersIn() =
    this@teamWithMaxTransfersIn.teamWithMaxTransfers(
        { gs: GameSeason -> gs.to.name.trim() != "" },
        { gs: GameSeason -> gs.to.name.trim() }
    )

fun List<GameSeason>.teamWithMaxTransfersOut() =
    this@teamWithMaxTransfersOut.teamWithMaxTransfers(
        { gs -> gs.from.name.trim() != "" },
        { gs -> gs.from.name.trim() }
    )

fun main() {
    val xferData = loadData(Paths.get("transfers.json"))
    xferData.top10Transfers().forEach {
        println("${it.season} ** ${it.player.name} ** ${it.from.name} ** ${it.to.name} ** ${it.transfer.xferValue.format(2)}")
    }
    println("--**--".repeat(15))
    println(xferData.teamWithMaxTransfersIn())
    println("--**--".repeat(15))
    println(xferData.teamWithMaxTransfersOut())
    println("--**--".repeat(15))
}