from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsLineString,
    QgsWkbTypes,
    QgsFeatureRequest
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QInputDialog
import math

# funcao para criar linhas perpendiculares
def create_perpendicular_lines(line, distance, length):
    perp_lines = []
    line_length = line.length()
    
    num_perp_lines = int(line_length / distance)
    
    for i in range(num_perp_lines + 1):
        accumulated_distance = i * distance
        point = line.interpolate(accumulated_distance)
        if not point:
            continue
        
        point_geom = point.asPoint()
        
        if accumulated_distance + distance < line_length:
            next_point = line.interpolate(accumulated_distance + distance).asPoint()
        else:
            next_point = line.interpolate(line_length).asPoint()
        
        dx = next_point.x() - point_geom.x()
        dy = next_point.y() - point_geom.y()
        
        angle = math.atan2(dy, dx)
        
        perp_angle1 = angle + math.pi / 2
        perp_angle2 = angle - math.pi / 2
        
        dx1 = length / 2 * math.cos(perp_angle1)
        dy1 = length / 2 * math.sin(perp_angle1)
        dx2 = length / 2 * math.cos(perp_angle2)
        dy2 = length / 2 * math.sin(perp_angle2)
        
        p1 = QgsPointXY(point_geom.x() + dx1, point_geom.y() + dy1)
        p2 = QgsPointXY(point_geom.x() + dx2, point_geom.y() + dy2)
        
        perp_line = QgsLineString([p1, p2])
        perp_lines.append((perp_line, accumulated_distance))
    
    return perp_lines


def main():
    # Get the active layer
    layer = iface.activeLayer()
    
    # Check if the layer is a line layer
    if layer.geometryType() != QgsWkbTypes.LineGeometry:
        iface.messageBar().pushMessage("Error", "Active layer is not a line layer", level=3)
        return
    
    # Parameters
    distance, ok1 = QInputDialog.getDouble(None, "Input Distance", "Enter the distance between perpendicular lines:", 10, 0, 10000, 2)
    if not ok1:
        return
    
    length, ok2 = QInputDialog.getDouble(None, "Input Length", "Enter the length of the perpendicular lines:", 10, 0, 10000, 2)
    if not ok2:
        return
    
    # Create a new memory layer for the perpendicular lines
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("distance", QVariant.Double))
    
    perp_layer = QgsVectorLayer("LineString?crs=" + layer.crs().authid(), "Perpendicular Lines", "memory")
    perp_layer_data = perp_layer.dataProvider()
    perp_layer_data.addAttributes(fields)
    perp_layer.updateFields()
    
    features = layer.getFeatures(QgsFeatureRequest())
    
    id_counter = 0
    
    for feature in features:
        geom = feature.geometry()
        if geom.type() == QgsWkbTypes.LineGeometry:
            if geom.isMultipart():
                lines = geom.asMultiPolyline()
            else:
                lines = [geom.asPolyline()]
            
            for line in lines:
                line_geom = QgsGeometry.fromPolylineXY(line)
                perp_lines = create_perpendicular_lines(line_geom, distance, length)
                
                for perp_line, accumulated_distance in perp_lines:
                    perp_feature = QgsFeature()
                    perp_feature.setGeometry(QgsGeometry(perp_line))
                    perp_feature.setAttributes([id_counter, accumulated_distance])
                    perp_layer_data.addFeature(perp_feature)
                    id_counter += 1
    
    QgsProject.instance().addMapLayer(perp_layer)

    # Label settings
    pal_layer = QgsPalLayerSettings()
    pal_layer.fieldName = "distance"
    pal_layer.placement = QgsPalLayerSettings.Line
       
    pal_layer.isExpression = False
    pal_layer.displayAll = True
    pal_layer.enabled = True
    
    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(1)
    buffer_settings.setColor(QColor("white"))
    text_format = QgsTextFormat()
    text_format.setBuffer(buffer_settings)

    pal_layer.setFormat(text_format)
    
    # Definir as propriedades de dados definidos para ancorar os rótulos no final da linha
    data_defined_properties = QgsPropertyCollection()
    data_defined_properties.setProperty(QgsPalLayerSettings.PositionX, QgsProperty.fromExpression("x(line_interpolate_point($geometry, length($geometry)))"))
    data_defined_properties.setProperty(QgsPalLayerSettings.PositionY, QgsProperty.fromExpression("y(line_interpolate_point($geometry, length($geometry)))"))
    pal_layer.setDataDefinedProperties(data_defined_properties)

    labeling = QgsVectorLayerSimpleLabeling(pal_layer)
    perp_layer.setLabeling(labeling)
    perp_layer.setLabelsEnabled(True)
    perp_layer.triggerRepaint()

    
    iface.messageBar().pushMessage("Success", "Perpendicular lines created successfully", level=1)

main()
