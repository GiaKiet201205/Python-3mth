async function readDataFile(filename) {
    const fs = require('fs').promises;
    const path = require('path');

    // Đường dẫn tuyệt đối đến thư mục data
    const baseDir = path.join(__dirname, '..', '..', 'data');
    const filePath = path.join(baseDir, filename);

    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error(`Lỗi đọc file ${filename}:`, error);
        throw error;
    }
}

async function writeDataFile(filename, data) {
    const fs = require('fs').promises;
    const path = require('path');
    const filePath = path.join(__dirname, '..', 'data', filename);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Hoán đổi orders giữa 2 drivers
 * @param {Array} selectedDrivers - Mảng 2 drivers cần switch
 * @returns {Object} Kết quả switch
 */
function switchDrivers(selectedDrivers) {
    const validation = validateSwitchConditions(selectedDrivers);
    if (!validation.valid) {
        return { success: false, message: validation.message };
    }

    const [driver1, driver2] = selectedDrivers;

    const driver1Orders = [...driver1.orders];
    const driver2Orders = [...driver2.orders];

    // Hoán đổi orders giữa 2 drivers
    [driver1.orders, driver2.orders] = [driver2.orders, driver1.orders];

    return {
        success: true,
        message: `Đã hoán đổi orders thành công!`,
        details: {
            driver1: {
                id: driver1.id,
                oldOrders: driver1Orders,
                newOrders: driver1.orders
            },
            driver2: {
                id: driver2.id,
                oldOrders: driver2Orders,
                newOrders: driver2.orders
            }
        }
    };
}

function validateConditions(conditions) {
    const { minItems, maxItems, requiredFields, customChecks } = conditions;

    if (minItems !== undefined && (!conditions.items || conditions.items.length < minItems)) {
        return { valid: false, message: conditions.minMessage };
    }

    if (maxItems !== undefined && conditions.items && conditions.items.length > maxItems) {
        return { valid: false, message: conditions.maxMessage };
    }

    if (requiredFields) {
        for (const field of requiredFields) {
            if (!field.value || !field.value[field.key]) {
                return { valid: false, message: field.message };
            }
        }
    }

    if (customChecks) {
        for (const check of customChecks) {
            if (!check.condition) {
                return { valid: false, message: check.message };
            }
        }
    }

    return { valid: true, message: conditions.successMessage };
}

function validateSwitchConditions(selectedDrivers) {
    return validateConditions({
        minItems: 2,
        maxItems: 2,
        minMessage: 'Vui lòng chọn 2 drivers để thực hiện switch!',
        maxMessage: 'Chỉ được chọn tối đa 2 drivers để thực hiện switch!',
        requiredFields: [
            { key: 'id', value: selectedDrivers?.[0], message: 'Thông tin driver không hợp lệ!' },
            { key: 'orders', value: selectedDrivers?.[0], message: 'Thông tin driver không hợp lệ!' },
            { key: 'id', value: selectedDrivers?.[1], message: 'Thông tin driver không hợp lệ!' },
            { key: 'orders', value: selectedDrivers?.[1], message: 'Thông tin driver không hợp lệ!' }
        ],
        customChecks: [
            { condition: selectedDrivers[0].id !== selectedDrivers[1].id, message: 'Vui lòng chọn 2 drivers khác nhau!' }
        ],
        successMessage: 'Điều kiện hợp lệ để thực hiện switch!'
    });
}

function getSwitchConfirmationInfo(selectedDrivers) {
    if (selectedDrivers.length !== 2) {
        return 'Vui lòng chọn đúng 2 drivers!';
    }

    const driver1 = selectedDrivers[0];
    const driver2 = selectedDrivers[1];

    let info = `Bạn có muốn hoán đổi orders giữa:\n\n`;
    info += `Driver ${driver1.id}:\n`;
    if (driver1.orders && driver1.orders.length > 0) {
        info += `  - Có ${driver1.orders.length} orders\n`;
    } else {
        info += `  - Chưa có orders\n`;
    }

    info += `Driver ${driver2.id}:\n`;
    if (driver2.orders && driver2.orders.length > 0) {
        info += `  - Có ${driver2.orders.length} orders\n`;
    } else {
        info += `  - Chưa có orders\n`;
    }

    info += `\nSau khi switch:\n`;
    info += `- Driver ${driver1.id} sẽ nhận orders từ Driver ${driver2.id}\n`;
    info += `- Driver ${driver2.id} sẽ nhận orders từ Driver ${driver1.id}`;

    return info;
}

// Xử lý sự kiện button Switch
async function switchButtonHandler(driverId1, driverId2) {
    try {
        const customers = await readDataFile('customers_qk7.json');
        const depots = await readDataFile('depots.json');

        const depot1 = depots.find(depot => depot.id === driverId1);
        const depot2 = depots.find(depot => depot.id === driverId2);

        if (!depot1 || !depot2) {
            return {
                success: false,
                message: 'Không tìm thấy thông tin driver/depot!'
            };
        }

        // Tạo dữ liệu driver với orders từ database
        const driver1 = {
            id: driverId1,
            name: depot1.name,
            orders: []
        };

        const driver2 = {
            id: driverId2,
            name: depot2.name,
            orders: []
        };
        const validation = validateSwitchConditions([driver1, driver2]);
        if (!validation.valid) {
            return {
                success: false,
                message: validation.message
            };
        }
        // Thực hiện switch orders
        const switchResult = await switchDrivers([driver1, driver2]);

        if (switchResult.success) {

            const confirmationInfo = getSwitchConfirmationInfo([driver1, driver2]);
            return {
                success: true,
                message: 'Switch thành công!',
                details: switchResult.details,
                confirmationInfo: confirmationInfo,
                depot1: depot1,
                depot2: depot2
            };
        } else {
            return switchResult;
        }

    } catch (error) {
        console.error('Lỗi khi xử lý button switch:', error);
        return {
            success: false,
            message: 'Có lỗi xảy ra: ' + error.message
        };
    }
}

/**
 * Lấy danh sách tất cả drivers (depots) để hiển thị
 * @returns {Promise<Array>} Danh sách drivers
 */
async function getAllDrivers() {
    try {
        const depots = await readDataFile('depots.json');
        return depots.map(depot => ({
            id: depot.id,
            name: depot.name,
            latitude: depot.latitude,
            longitude: depot.longitude
        }));
    } catch (error) {
        console.error('Lỗi khi lấy danh sách drivers:', error);
        throw error;
    }
}
/**
 * Hàm lấy thông tin chi tiết của một driver
 * @param {number} driverId - ID của driver
 * @returns {Promise<Object>} Thông tin chi tiết driver
 */
async function getDriverDetails(driverId) {
    try {
        const customers = await readDataFile('customers_qk7.json');
        const depots = await readDataFile('depots.json');

        const depot = depots.find(d => d.id === driverId);
        if (!depot) {
            throw new Error('Không tìm thấy driver!');
        }

        const orders = [];

        return {
            id: depot.id,
            name: depot.name,
            latitude: depot.latitude,
            longitude: depot.longitude,
            orders: orders
        };
    } catch (error) {
        console.error('Lỗi khi lấy thông tin driver:', error);
        throw error;
    }
}

/**
 * Hàm đảo ngược thứ tự route của một driver
 * @param {Object} driver - Thông tin driver cần reverse route
 * @returns {Object} Kết quả thực hiện reverse
 */
function reverseDriverRoute(driver) {
    const validation = validateReverseConditions(driver);
    if (!validation.valid) {
        return { success: false, message: validation.message };
    }

    const originalOrders = [...driver.orders];
    const middleOrders = driver.orders.slice(1, -1);
    const reversedMiddleOrders = middleOrders.reverse();
    driver.orders = [
        driver.orders[0],
        ...reversedMiddleOrders,
        driver.orders[driver.orders.length - 1]
    ];

    return {
        success: true,
        message: `Đã đảo ngược route thành công!`,
        details: {
            driver: {
                id: driver.id,
                originalRoute: originalOrders,
                reversedRoute: driver.orders
            }
        }
    };
}

function validateReverseConditions(driver) {
    return validateConditions({
        requiredFields: [
            { key: 'id', value: driver, message: 'Vui lòng chọn một driver!' },
            { key: 'orders', value: driver, message: 'Driver chưa có orders để reverse!' }
        ],
        customChecks: [
            {
                condition: !driver.orders || driver.orders.length <= 2,
                message: 'Route quá ngắn để thực hiện reverse!'
            }
        ],
        successMessage: 'Điều kiện hợp lệ để thực hiện reverse!'
    });
}

function getReverseConfirmationInfo(driver) {
    if (!driver || !driver.orders) {
        return 'Vui lòng chọn một driver có orders!';
    }
    let info = `Bạn có muốn đảo ngược route của:\n\n`;
    info += `Driver ${driver.id} (${driver.name || 'N/A'}):\n\n`;

    info += `Route hiện tại:\n`;
    driver.orders.forEach((order, index) => {
        const pointType = index === 0 || index === driver.orders.length - 1 ? 'Depot' : 'Customer';
        const pointName = order.customerName || order.name || `Điểm ${order.id}`;
        info += `  ${index + 1}. ${pointType}: ${pointName}\n`;
    });
    info += `\nRoute sau khi reverse:\n`;
    const reversedOrders = [
        driver.orders[0],
        ...driver.orders.slice(1, -1).reverse(),
        driver.orders[driver.orders.length - 1]
    ];

    reversedOrders.forEach((order, index) => {
        const pointType = index === 0 || index === reversedOrders.length - 1 ? 'Depot' : 'Customer';
        const pointName = order.customerName || order.name || `Điểm ${order.id}`;
        info += `  ${index + 1}. ${pointType}: ${pointName}\n`;
    });

    return info;
}
/**
 * Hàm xử lý sự kiện button Reverse Route
 * @param {number} driverId
 * @returns {Promise<Object>}
 */
async function reverseButtonHandler(driverId) {
    try {
        const customers = await readDataFile('customers_qk7.json');
        const depots = await readDataFile('depots.json');
        const depot = depots.find(d => d.id === driverId);
        if (!depot) {
            return {
                success: false,
                message: 'Không tìm thấy thông tin driver/depot!'
            };
        }

        const driver = {
            id: driverId,
            name: depot.name,
            orders: []
        };

        const validation = validateReverseConditions(driver);
        if (!validation.valid) {
            return {
                success: false,
                message: validation.message
            };
        }

        // Thực hiện reverse route
        const reverseResult = await reverseDriverRoute(driver);

        if (reverseResult.success) {
            const confirmationInfo = getReverseConfirmationInfo(driver);
            return {
                success: true,
                message: 'Reverse route thành công!',
                details: reverseResult.details,
                confirmationInfo: confirmationInfo,
                depot: depot
            };
        } else {
            return reverseResult;
        }

    } catch (error) {
        console.error('Lỗi khi xử lý button reverse:', error);
        return {
            success: false,
            message: 'Có lỗi xảy ra: ' + error.message
        };
    }
}

function getOrderDate(order) {
    if (order.date) {
        return order.date;
    }
    if (order.createdAt) {
        return new Date(order.createdAt).toISOString().split('T')[0];
    }
    if (order.deliveryDate) {
        return new Date(order.deliveryDate).toISOString().split('T')[0];
    }
    return null;
}

// CHỨC NĂNG LỌC THEO NGÀY THÁNG
function filterOrdersByDate(orders, date) {
    if (!orders || !Array.isArray(orders) || !date || typeof date !== 'string') {
        return orders || [];
    }

    return orders.filter(order => getOrderDate(order) === date);
}
function filterOrdersByDateRange(orders, startDate, endDate) {
    if (!orders || !Array.isArray(orders) || !startDate || !endDate) {
        return orders || [];
    }
    return orders.filter(order => {
        const orderDate = getOrderDate(order);
        return orderDate && orderDate >= startDate && orderDate <= endDate;
    });
}

function filterOrdersByMonthYear(orders, month, year) {
    if (!orders || !Array.isArray(orders) || !month || !year || month < 1 || month > 12) {
        return orders || [];
    }
    return orders.filter(order => {
        const orderDateStr = getOrderDate(order);
        if (!orderDateStr) return false;

        const orderDate = new Date(orderDateStr);
        return orderDate.getMonth() + 1 === month && orderDate.getFullYear() === year;
    });
}

function getDatesWithOrders(orders) {
    if (!orders || !Array.isArray(orders)) {
        return [];
    }
    const dates = new Set();
    orders.forEach(order => {
        const orderDate = getOrderDate(order);
        if (orderDate) {
            dates.add(orderDate);
        }
    });
    return Array.from(dates).sort();
}

function validateDateFilterConditions(startDate, endDate) {
    if (startDate && endDate && startDate > endDate) {
        return {
            valid: false,
            message: 'Ngày bắt đầu không được lớn hơn ngày kết thúc!'
        };
    }
    if (startDate && !isValidDateFormat(startDate)) {
        return {
            valid: false,
            message: 'Định dạng ngày bắt đầu không hợp lệ! Sử dụng định dạng YYYY-MM-DD'
        };
    }
    if (endDate && !isValidDateFormat(endDate)) {
        return {
            valid: false,
            message: 'Định dạng ngày kết thúc không hợp lệ! Sử dụng định dạng YYYY-MM-DD'
        };
    }
    return {
        valid: true,
        message: 'Điều kiện lọc hợp lệ!'
    };
}

function isValidDateFormat(dateString) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    if (!regex.test(dateString)) {
        return false;
    }
    const date = new Date(dateString);
    const [year, month, day] = dateString.split('-').map(Number);

    return date.getFullYear() === year &&
           date.getMonth() === month - 1 &&
           date.getDate() === day;
}


function getDateFilterInfo(filterType, filterParams) {
    let info = 'Thông tin lọc orders:\n\n';
    switch (filterType) {
        case 'date':
            info += `Lọc theo ngày: ${filterParams.date}\n`;
            break;
        case 'range':
            info += `Lọc từ ngày: ${filterParams.startDate}\n`;
            info += `Đến ngày: ${filterParams.endDate}\n`;
            break;
        case 'month':
            info += `Lọc theo tháng: ${filterParams.month}/${filterParams.year}\n`;
            break;
        default:
            info += 'Không xác định loại lọc\n';
    }

    return info;
}
/**
 * Hàm xử lý lọc orders theo ngày tháng
 * @param {Array} orders - Danh sách orders cần lọc
 * @param {Object} filterOptions - Tùy chọn lọc
 * @returns {Promise<Object>} Kết quả lọc
 */
async function filterOrdersByDateHandler(orders, filterOptions) {
    try {
        if (!orders || !Array.isArray(orders)) {
            return {
                success: false,
                message: 'Danh sách orders không hợp lệ!'
            };
        }
        const { filterType, date, startDate, endDate, month, year } = filterOptions;
        if (!filterType) {
            return {
                success: false,
                message: 'Vui lòng chọn loại lọc!'
            };
        }
        let filteredOrders = [];
        let filterInfo = '';
        switch (filterType) {
            case 'date':
                if (!date) {
                    return {
                        success: false,
                        message: 'Vui lòng nhập ngày cần lọc!'
                    };
                }
                const validation = validateDateFilterConditions(date, null);
                if (!validation.valid) {
                    return {
                        success: false,
                        message: validation.message
                    };
                }
                filteredOrders = filterOrdersByDate(orders, date);
                filterInfo = getDateFilterInfo('date', { date });
                break;
            case 'range':
                if (!startDate || !endDate) {
                    return {
                        success: false,
                        message: 'Vui lòng nhập đầy đủ ngày bắt đầu và kết thúc!'
                    };
                }
                const rangeValidation = validateDateFilterConditions(startDate, endDate);
                if (!rangeValidation.valid) {
                    return {
                        success: false,
                        message: rangeValidation.message
                    };
                }
                filteredOrders = filterOrdersByDateRange(orders, startDate, endDate);
                filterInfo = getDateFilterInfo('range', { startDate, endDate });
                break;
            case 'month':
                if (!month || !year) {
                    return {
                        success: false,
                        message: 'Vui lòng nhập đầy đủ tháng và năm!'
                    };
                }
                filteredOrders = filterOrdersByMonthYear(orders, month, year);
                filterInfo = getDateFilterInfo('month', { month, year });
                break;
            default:
                return {
                    success: false,
                    message: 'Loại lọc không hợp lệ!'
                };
        }

        return {
            success: true,
            message: `Lọc thành công! Tìm thấy ${filteredOrders.length} orders.`,
            filteredOrders: filteredOrders,
            filterInfo: filterInfo,
            totalOrders: orders.length,
            filteredCount: filteredOrders.length
        };
    } catch (error) {
        console.error('Lỗi khi lọc orders theo ngày:', error);
        return {
            success: false,
            message: 'Có lỗi xảy ra khi lọc: ' + error.message
        };
    }
}

function getOrdersStatsByDate(orders) {
    if (!orders || !Array.isArray(orders)) {
        return {};
    }
    const stats = {};
    orders.forEach(order => {
        const orderDate = getOrderDate(order);
        if (orderDate) {
            if (!stats[orderDate]) {
                stats[orderDate] = { count: 0, orders: [] };
            }
            stats[orderDate].count++;
            stats[orderDate].orders.push(order);
        }
    });
    return stats;
}

module.exports = {
    switchDrivers,
    validateSwitchConditions,
    getSwitchConfirmationInfo,
    readDataFile,
    writeDataFile,
    switchButtonHandler,
    getAllDrivers,
    getDriverDetails,
    reverseDriverRoute,
    validateReverseConditions,
    getReverseConfirmationInfo,
    reverseButtonHandler,
    filterOrdersByDate,
    filterOrdersByDateRange,
    filterOrdersByMonthYear,
    getDatesWithOrders,
    validateDateFilterConditions,
    isValidDateFormat,
    getDateFilterInfo,
    filterOrdersByDateHandler,
    getOrdersStatsByDate
};