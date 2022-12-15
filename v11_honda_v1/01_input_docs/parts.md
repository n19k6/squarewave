Component | Type | Manufacturer | Mouserpart-Nr | Productpage | Datasheet
--------       | --------  | -------- | -------- | --------| --------
R2R ladder     | PmodR2R   | Digilent | 485-239  | [R2R ladder](https://digilent.com/shop/pmod-r2r-resistor-ladder-d-a-converter/) | [Schematic](https://digilent.com/reference/_media/reference/pmod/pmodr2r/pmodr2r_sch.pdf)
DAC    | DAC0808LCN/NOP | TI   | [926-DAC0808LCN/NOPB](https://www.mouser.de/ProductDetail/Texas-Instruments/DAC0808LCN-NOPB?qs=7X5t%252BdzoRHDv8TW%252BETgvcg%3D%3D) | - | -
Dual 10bit DAC w/SPI     | MCP4812-E/P   | Microchip | [579-MCP4812-E/P](https://www.mouser.de/ProductDetail/Microchip-Technology-Atmel/MCP4812-E-P?qs=bxUt0k7cytI17caZuUAwlA%3D%3D)  | -| -
Dual 8bit DAC w/SPI     | MCP4802-E/P   | Microchip | [579-MCP4802-E/P](https://www.mouser.de/ProductDetail/Microchip-Technology-Atmel/MCP4802-E-P?qs=bxUt0k7cytI0U0E3kiOWig%3D%3D)  | -| -
MCP4725 Breakout     | MCP4725 | Adafruit | [485-935](https://www.mouser.de/ProductDetail/Adafruit/935?qs=GURawfaeGuDLSBaw80Z3Sg%3D%3D)  | [MCP4725 Breakout](https://www.adafruit.com/product/935)| [Datasheet](https://cdn-shop.adafruit.com/datasheets/mcp4725.pdf)

R2R ladder     | PmodR2R   | Digilent | 485-239  | []() | []()
R2R ladder     | PmodR2R   | Digilent | 485-239  | []() | []()

Possible next steps:
- use R2R ladder and generate sine-wave using DMA on pico
  - how to connect Pmod R2R with pico (schematics)
  - how to meassure voltage with osciloscope
- connect one of the ics using an interface like i2c or spi
  - DAC0808LCN/NOP might be similiar to r2r ladder circuit
